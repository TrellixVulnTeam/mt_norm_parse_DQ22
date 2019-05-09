from env.importing import *
from io_.dat.constants import TOKEN_BPE_BERT_SEP, TOKEN_BPE_BERT_START, PAD_ID_BERT, PAD_BERT, PAD_ID_NORM_NOT_NORM
from io_.info_print import printing

from toolbox.sanity_check import sanity_check_data_len


def preprocess_batch_string_for_bert(batch):
    """
    adding starting and ending token in raw sentences
    :param batch:
    :return:
    """
    for i in range(len(batch)):
        batch[i][0] = TOKEN_BPE_BERT_START
        batch[i][-1] = TOKEN_BPE_BERT_SEP
        batch[i] = " ".join(batch[i])
    return batch


def get_indexes(list_pretokenized_str, tokenizer, verbose, use_gpu,
                word_norm_not_norm=None):
    """
    from pretokenized string : it will bpe-tokenize it using BERT 'tokenizer'
    and then convert it to tokens ids
    :param list_pretokenized_str:
    :param tokenizer:
    :param verbose:
    :param use_gpu:
    :return:
    """
    all_tokenized_ls = [tokenizer.tokenize(inp) for inp in list_pretokenized_str]
    tokenized_ls = [tup[0] for tup in all_tokenized_ls]
    aligned_index = [tup[1] for tup in all_tokenized_ls]
    segments_ids = [[0 for _ in range(len(tokenized))] for tokenized in tokenized_ls]

    printing("DATA : bpe tokenized {}", var=[tokenized_ls], verbose=verbose, verbose_level="raw_data")

    ids_ls = [tokenizer.convert_tokens_to_ids(inp) for inp in tokenized_ls]
    max_sent_len = max([len(inp) for inp in tokenized_ls])
    ids_padded = [inp + [PAD_ID_BERT for _ in range(max_sent_len - len(inp))] for inp in ids_ls]
    aligned_index_padded = [[e for e in inp] + [1000 for _ in range(max_sent_len - len(inp))] for inp in aligned_index]
    segments_padded = [inp + [PAD_ID_BERT for _ in range(max_sent_len - len(inp))] for inp in segments_ids]

    def mask_group(norm_not_norm, bpe_aligned_index):
        """
        norm_not_norm : 1 if group to mask (need_norm) 0 if normed
        can be use with any group of token to mask
        """
        mask_batch = []
        for i_sent, sent in enumerate(bpe_aligned_index):
            mask_sent = []
            for i in range(len(sent)):
                original_index = sent[i]
                norm_not = norm_not_norm[i_sent, original_index]
                mask_sent.append(1 - norm_not if norm_not != PAD_ID_NORM_NOT_NORM
                                 else PAD_ID_NORM_NOT_NORM)

            mask_batch.append(mask_sent)
        return mask_batch

    if word_norm_not_norm is not None:
        mask = mask_group(word_norm_not_norm, bpe_aligned_index=aligned_index_padded)
    else:
        mask = [[1 for _ in inp]+[0 for _ in range(max_sent_len - len(inp))] for inp in segments_ids]
    mask = torch.LongTensor(mask)
    tokens_tensor = torch.LongTensor(ids_padded)
    segments_tensors = torch.LongTensor(segments_padded)
    if use_gpu:
        mask = mask.cuda()
        tokens_tensor = tokens_tensor.cuda()
        segments_tensors = segments_tensors.cuda()

    printing("DATA {}", var=[tokens_tensor], verbose=verbose, verbose_level=3)

    sanity_check_data_len(tokens_tensor, segments_tensors, tokenized_ls, aligned_index, raising_error=True)

    return tokens_tensor, segments_tensors, tokenized_ls, aligned_index_padded, mask


def from_bpe_token_to_str(
                          bpe_tensor, topk, pred_mode,
                          null_token_index, null_str,
                          tokenizer=None, pos_dictionary=None,
                          task="normalize"
                          ):
    """
    it actually supports not only bpe token but also pos-token
    pred_mode allow to handle gold data also (which only have 2 dim and not three)
    :param bpe_tensor:
    :param topk: int : number of top prediction : will arrange them with all the top1 all the 2nd all the third...
    :param pred_mode: book
    :return:
    """
    predictions_topk_ls = [[[bpe_tensor[sent, word, top].item() if pred_mode else bpe_tensor[sent, word].item()
                             for word in range(bpe_tensor.size(1))] for sent in range(bpe_tensor.size(0))]
                           for top in range(topk)]
    if task == "normalize":
        assert tokenizer is not None
        sent_ls_top = [[tokenizer.convert_ids_to_tokens(sent_bpe, special_extra_token=null_token_index,
                                                        special_token_string=null_str) for sent_bpe in predictions_topk]
                       for predictions_topk in predictions_topk_ls]
    elif task == "pos":
        # NB +1 because index 0 is related to UNK
        #print("DEBUG", predictions_topk_ls, len(pos_dictionary.instances))
        sent_ls_top = [[[pos_dictionary.instances[token_ind-1] if token_ind > 0 else "UNK"
                         for token_ind in sent_bpe] for sent_bpe in predictions_topk]
                       for predictions_topk in predictions_topk_ls]
    if not pred_mode:
        sent_ls_top = sent_ls_top[0]
    return sent_ls_top
