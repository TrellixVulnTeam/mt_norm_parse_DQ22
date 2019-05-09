from evaluate.scoring.compute_score import word_level_scoring, word_level_filter
from evaluate.scoring.aggregate_score import agg_func_batch_score

AVAILABLE_EVALUATION_SAMPLE_FILTER = ["all"]


def overall_word_level_metric_measure(gold_sent_ls,
                                      pred_sent_ls_topk, topk,
                                      metric="exact_match",
                                      samples=None,
                                      src_detokenized=None,
                                      reference_word_dic=None,
                                      agg_func_ls=None):
    """
    'metric' based on a word level comparison of (pred,gold) : e.g : exact_match , edit
    'agg_func' based on a aggregation func to get the overall batch score : e.g : sum
    :param metric:
    :param agg_func:
    :return batch : score, number of token measured
    """
    if samples is None:
        samples = ["all"]
    if agg_func_ls is None:
        agg_func_ls = ["sum"]

    assert isinstance(samples, list)
    assert len(set(samples) & set(AVAILABLE_EVALUATION_SAMPLE_FILTER)) > 0, \
        "ERROR : one of the samples in {} not supported {}".format(samples, AVAILABLE_EVALUATION_SAMPLE_FILTER)

    assert isinstance(agg_func_ls, list)
    assert len(pred_sent_ls_topk) == topk, "ERROR topk not consistent with prediction list " \
        .format(len(pred_sent_ls_topk), topk)
    overall_score_ls_sent = []
    overall_filter_ls = {sample: [] for sample in samples}

    skipping_sent = 0
    for gold_ind_sent, gold_sent in enumerate(gold_sent_ls):
        # TODO test for all topk
        try:
            assert len(gold_sent) == len(pred_sent_ls_topk[0][gold_ind_sent])
        except Exception as e:
            print(e)
            skipping_sent += len(gold_sent_ls)
            overall_score_ls_sent = [[0]]
            break
        if src_detokenized is not None:
            assert len(gold_sent) == len(src_detokenized[gold_ind_sent]), \
                "ERROR src_detokenized and gold_sent_ls for sent {} have different length ".format(gold_sent)
        score_sent = []
        filter_sent = {_sample: [] for _sample in samples}
        for ind_word in range(len(gold_sent)):
            gold_token = gold_sent[ind_word]
            topk_word_pred = [pred_sent_ls_topk[top][gold_ind_sent][ind_word] for top in range(topk)]
            score_sent.append(word_level_scoring(metric=metric, gold=gold_token, topk_pred=topk_word_pred, topk=topk))
            for _sample in samples:
                filter_sent[_sample].append(word_level_filter(sample=_sample, gold=gold_token, topk_pred=topk_word_pred,
                                                              topk=topk, src=src_detokenized[gold_ind_sent][ind_word],
                                                              word_reference_dic_ls=reference_word_dic))
        for _sample in samples:
            overall_filter_ls[_sample].append(filter_sent[_sample])
        overall_score_ls_sent.append(score_sent)

    result = {agg_func: {} for agg_func in agg_func_ls}

    for agg_func in agg_func_ls:
        for sample in samples:
            result[agg_func][sample] = {"score": agg_func_batch_score(overall_ls_sent_score=overall_score_ls_sent,
                                                                      agg_func=agg_func,
                                                                      overall_filter=overall_filter_ls[sample]),
                                        "agg_func": agg_func,
                                        "metric": "exact_match",
                                        "n_tokens": agg_func_batch_score(overall_ls_sent_score=overall_score_ls_sent,
                                                                         overall_filter=overall_filter_ls[sample],
                                                                         agg_func="n_tokens"),
                                        "n_sents": agg_func_batch_score(overall_ls_sent_score=overall_score_ls_sent,
                                                                        overall_filter=overall_filter_ls[sample],
                                                                        agg_func="n_sents")}
            print("SAMPLE", result[agg_func][sample] )
    return result, skipping_sent
