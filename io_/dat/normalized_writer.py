from io_.info_print import printing
from io_.dat.constants import SPECIAL_TOKEN_LS
from env.importing import *

APPLY_PERMUTE_THRESHOLD_SENT = 0.8
APPLY_PERMUTE_WORD = 0.8


def write_conll(format, dir_normalized, dir_original, src_text_ls, text_decoded_ls,
                src_text_pos, pred_pos_ls, tasks, inverse=False,permuting_mode=None, cp_paste=False,
                ind_batch=0, new_file=False, cut_sent=False, verbose=0):
    assert format in ["conll"]
    #assert len(tasks) == 1, "ERROR : only supported so far 1 task at a time"

    if tasks[0] == "normalize":
        src_ls = src_text_ls
        pred_ls = text_decoded_ls
        if text_decoded_ls is None:
            assert permuting_mode is not None or cp_paste
            pred_ls = src_text_ls
    elif tasks[0] == "pos":
        src_ls = src_text_pos
        pred_ls = pred_pos_ls
    if format == "conll":
        mode_write = "w" if new_file else "a"
        if new_file:
            printing("CREATING NEW FILE (io_/dat/normalized_writer) : {} ", var=[dir_normalized], verbose=verbose, verbose_level=1)
        with open(dir_normalized, mode_write) as norm_file:
            with open(dir_original, mode_write) as original:
                len_original = 0
                for ind_sent, (original_sent, normalized_sent) in enumerate(zip(src_ls, pred_ls)):
                    try:
                        assert len(original_sent) == len(normalized_sent), "WARNING : (writer) original_sent len {} {} \n  " \
                                                                           "normalized_sent len {} {} ".format(len(original_sent), original_sent, len(normalized_sent), normalized_sent)
                    except AssertionError as e:
                        print(e)
                        if len(original_sent) > len(normalized_sent):
                            normalized_sent.extend(["UNK" for _ in range(len(original_sent)-len(normalized_sent))])
                            print("WARNING (writer) : original larger than prediction : so appending UNK token for writing")
                        else:
                            print("WARNING (writer) : original smaller than prediction ! ")

                    norm_file.write("#\n")
                    original.write("#\n")
                    norm_file.write("#sent_id = {} \n".format(ind_sent+ind_batch+1))
                    original.write("#sent_id = {} \n".format(ind_sent+ind_batch+1))
                    ind_adjust = 0

                    if permuting_mode == "sample_mode":
                        noise_level_sentence = np.random.random(1)[0]

                    for ind, (original_token, normalized_token) in enumerate(zip(original_sent,
                                                                                 normalized_sent)):
                        # WE REMOVE SPECIAL TOKENS ONLY IF THEY APPEAR AT THE BEGINING OR AT THE END
                        # on the source token !! (it tells us when we stop) (we nevern want to use gold information)
                        max_len_word = max(len(original_token),len_original)
                        if original_token in SPECIAL_TOKEN_LS and (ind+1 == len(original_sent) or ind == 0):
                            ind_adjust = 1
                            continue

                        if permuting_mode == "sample_mode":
                            # 20% of sentences we apply a 80 noise level n 80% of cases only a 20% noise level
                            rand_word = np.random.random(1)[0]
                            threshold_word = 0.8 if noise_level_sentence < 0.2 else 0.2
                            if rand_word < threshold_word:
                                permuting_mode = np.random.choice(["permute", "double", "random_replace",
                                                                   "multiply_last", "double_last","remove",
                                                                   "remove_last", "z_replace_s"])
                            #print("PERMUTATION is ", permuting_mode, rand_word, APPLY_PERMUTE_WORD,noise_level_sentence)

                        else:
                            rand_word = None

                        # TODO : when want simultanuous training : assert src_pos src_norm same
                        #   --> assert pred_pos and pred_norm are same lengh (number of words) ans write
                        if tasks[0] == "normalize":
                            if inverse:
                                assert not cp_paste
                                _original_token = normalized_token
                                _normalized_token = original_token

                            else:
                                _original_token = original_token
                                _normalized_token = normalized_token
                                if permuting_mode is not None:
                                    assert not cp_paste
                                    # rule one
                                    #print("ORIGINAL TOKEN", original_token)
                                    if ( _original_token == _normalized_token or _original_token.lower() == _normalized_token.lower())\
                                        and not (original_token.startswith("#") or original_token.startswith("@")):
                                        # rule 1
                                        if permuting_mode == "z_replace_s" and len(original_token) > 1:
                                            if original_token.endswith("s"):
                                                _original_token = original_token[:-1] + "z"
                                            else:
                                                permuting_mode = np.random.choice(["permute", "double",
                                                                                   "random_replace",
                                                                                   "remove", "remove_last",
                                                                                   "multiply_last","double_last",
                                                                                    "z_replace_s"])

                                        if permuting_mode == "permute" and len(original_token) > 1:
                                            start_index = 0 if not (original_token.startswith("#") or original_token.startswith("@")) else 1
                                            to_permute = np.random.randint(start_index, len(original_token)-1)
                                            second_letter = original_token[to_permute+1]
                                            first_letter = original_token[to_permute]
                                            list_original_token = list(original_token)
                                            #pdb.set_trace()
                                            list_original_token[to_permute] = second_letter
                                            list_original_token[to_permute+1] = first_letter
                                            _original_token = "".join(list_original_token)
                                        # rule 2
                                        if (permuting_mode == "double" or permuting_mode == "remove") and len(original_token) > 1:
                                            start_index = 0
                                            to_double = np.random.randint(start_index, len(original_token)-1)
                                            first_letter = original_token[to_double]
                                            list_original_token = list(original_token)
                                            #pdb.set_trace()
                                            if permuting_mode == "double":
                                                list_original_token = list_original_token[:to_double] + [first_letter] + list_original_token[to_double:]
                                            else:
                                                list_original_token = list_original_token[:to_double] + list_original_token[to_double:]

                                            _original_token = "".join(list_original_token)

                                        if permuting_mode == "remove_last" and len(original_token) > 1:
                                            _original_token = _original_token[:-1]
                                        if permuting_mode == "double_last" and len(original_token) > 1:
                                            _original_token = _original_token+_original_token[-1]
                                        if permuting_mode == "random_replace" and len(original_token) > 1:
                                            start_index = 0
                                            to_replace = np.random.randint(start_index, len(original_token) - 1)
                                            random_letter = np.random.choice(list("abcdefghijklmnopqrstuvwxyz"))
                                            first_letter = original_token[to_replace]
                                            list_original_token = list(original_token)
                                            # pdb.set_trace()

                                            list_original_token[to_replace] = random_letter

                                            _original_token = "".join(list_original_token)



                                        #print("NEW TOKEN", permuting_mode, _original_token)

                                    #pdb.set_trace()

                            if cp_paste:
                                _normalized_token = _original_token

                            norm_file.write("{}\t{}\t_\t_\t_\t_\t{}\t_\t_\tNorm={}|\n".format(ind + 1 - ind_adjust,
                                                                                              _original_token,
                                                                                              ind - ind_adjust if ind - ind_adjust > 0 else 0,
                                                                                              _normalized_token))
                        if tasks[0] == "pos":
                            norm_file.write("{}\t{}\t_\t{}\t_\t_\t{}\t_\t_\tNorm=()|\n".format(ind + 1 - ind_adjust,
                                                                                               original_token,
                                                                                               normalized_token,
                                                                                               ind-ind_adjust if ind - ind_adjust > 0 else 0
                                                                                               ))
                        original.write("{}\t{}\t_\t_\t_\t_\t_\t_\t{}\t_\n".format(ind+1,
                                                                                  original_token,
                                                                                  ind - ind_adjust if ind - ind_adjust > 0 else 0))

                        if cut_sent:
                            if ind > 50:
                                break
                    norm_file.write("\n")
                    original.write("\n")
            printing("WRITING predicted batch of {} original and {} normalized",
                     var=[dir_original, dir_normalized], verbose=verbose, verbose_level="raw_data")

    return max_len_word


def write_conll_multitask(format, dir_pred, dir_original, src_text_ls,
                          pred_per_task, tasks,task_parameters, cp_paste=False, gold=False,
                          all_indexes=None,
                          ind_batch=0, new_file=False, cut_sent=False, verbose=0):

    assert format in ["conll"]
    max_len_word = None
    writing_top = 1
    # assert each task is predicting as many sample per batch
    pred_task_len_former = -1
    task_former = ""


    # assertion on number of samples predicted
    for task in pred_per_task:

        pred_task_len = len(pred_per_task[task]) if gold else len(pred_per_task[task][writing_top-1])

        if pred_task_len_former > 0:
            assert pred_task_len == pred_task_len_former, \
                "ERROR {} and {} task ".format(task_former, task)
            assert pred_task_len == len(src_text_ls["mwe_prediction"]),\
                "ERROR mismatch source mwe_prediction {}  and prediction {} ".format(src_text_ls, pred_per_task[task])
            assert pred_task_len == len(src_text_ls["wordpieces_inputs_raw_tokens"]), \
                "ERROR mismatch source wordpieces_inputs_raw_tokens {} and prediction {} ".format(src_text_ls, pred_per_task[task])
            try:
                assert pred_task_len == all_indexes.shape[0], "ERROR mismatch index {}  and all_indexes {} : pred {}".format(pred_task_len, all_indexes.shape[0], pred_per_task[task])
            except:
                pdb.set_trace()
        pred_task_len_former = pred_task_len

        task_former = task
        if format == "conll":
            mode_write = "w" if new_file else "a"
        if new_file:
            printing("CREATING NEW FILE (io_/dat/normalized_writer) : {} ", var=[dir_pred], verbose=verbose,
                     verbose_level=1)

    with open(dir_pred, mode_write) as norm_file:
        with open(dir_original, mode_write) as original:
            len_original = 0
            for ind_sent in range(all_indexes.shape[0]):

                pred_sent = OrderedDict()

                # NB : length assertion for each input-output (correcting if possible)
                for task in pred_per_task:

                    if gold:
                        pred_sent[task] = pred_per_task[task][ind_sent]
                    else:
                        pred_sent[task] = pred_per_task[task][writing_top-1][ind_sent]

                    try:
                        if task.startswith("parsing"):
                            src = src_text_ls["mwe_prediction"][ind_sent]
                        else:
                            src = src_text_ls[task_parameters[task]["input"]][ind_sent]
                        assert len(src) == len(pred_sent[task]),\
                            "WARNING : (writer) task {} original_sent len {} {} \n  predicted sent len {} {}".format(task,len(src), src, len(pred_sent[task]), pred_sent[task])
                    except AssertionError as e:
                        print(e)
                        if len(src) > len(pred_sent[task]):
                            pred_sent[task].extend(["UNK" for _ in range(len(src)-len(pred_sent[task]))])
                            print("WARNING (writer) : original larger than prediction : so appending UNK token for writing")
                        else:
                            print("WARNING (writer) : original smaller than prediction for ")

                norm_file.write("#\n")
                original.write("#\n")
                norm_file.write("#sent_id = {} \n".format(ind_sent+ind_batch+1))
                original.write("#sent_id = {} \n".format(ind_sent+ind_batch+1))
                ind_adjust = 0

                #for ind, original_token in enumerate(original_sent):
                last_mwe_index = -1
                adjust_mwe = 0
                for ind in all_indexes[ind_sent, :]:
                    # WE REMOVE SPECIAL TOKENS ONLY IF THEY APPEAR AT THE BEGINING OR AT THE END
                    # on the source token !! (it tells us when we stop) (we nevern want to use gold information)
                    if "-" in ind and ind != "-1":
                        matching_mwe_ind = re.match("([0-9]+)-([0-9]+)", str(ind))
                        assert matching_mwe_ind is not None, "ERROR ind is {} : could not found mwe index".format(ind)
                        last_mwe_index = int(matching_mwe_ind.group(2))
                        ind_mwe = int(matching_mwe_ind.group(1))
                        original_token = src_text_ls["wordpieces_inputs_raw_tokens"][ind_sent][ind_mwe]
                        adjust_mwe += (last_mwe_index-ind_mwe)
                        #assert ind_adjust == 0, "ERROR not supported"
                        mwe_meta = "Norm={}|mwe_detection={}|n_masks_mwe={}".format("_", pred_sent["mwe_detection"][ind_mwe] if "mwe_detection" in pred_per_task else "_",
                                                                                    pred_sent["n_masks_mwe"][ind_mwe] if "n_masks_mwe" in pred_per_task else "_")
                        norm_file.write("{index}\t{original}\t_\t{pos}\t_\t_\t{dep}\t_\t{types}\t{norm}\n".format(index=ind, original=original_token, pos="_", types="_", dep="_", norm=mwe_meta))
                        original.write("{}\t{}\t_\t_\t_\t_\t_\t_\t{}\t_\n".format(ind, original_token, "_"))
                        continue
                    else:
                        ind = int(ind)
                        original_token = src_text_ls["mwe_prediction"][ind_sent][ind]
                        # asserting that we have everything together on the source side
                        if ind > last_mwe_index:
                            assert src_text_ls["mwe_prediction"][ind_sent][ind] == src_text_ls["wordpieces_inputs_raw_tokens"][ind_sent][ind-adjust_mwe], "ERROR : on non-mwe tokens : raw and tokenized should be same but are raw {} tokenizd {}".format(src_text_ls["wordpieces_inputs_raw_tokens"][ind_sent][ind],src_text_ls["mwe_prediction"][ind_sent][ind+adjust_mwe])

                    max_len_word = max(len(original_token), len_original)
                    #if original_token in SPECIAL_TOKEN_LS and (ind+1 == len(original_sent) or ind == 0):
                    if original_token in SPECIAL_TOKEN_LS: #ind == "-1" or ind == 0 or original_token == "[SEP]":
                        # ind 0 is skipped because it corresponds to CLS
                        ind_adjust = 1
                        continue

                    pos = pred_sent["pos"][ind] if "pos" in pred_per_task else "_"
                    try:
                        tenth_col = "Norm={}|mwe_detection={}|n_masks_mwe={}".format(pred_sent["normalize"][ind] if "normalize" in pred_per_task else "_",
                                                                                 pred_sent["mwe_detection"][ind-adjust_mwe] if "mwe_detection" in pred_per_task else "_",
                                                                                 pred_sent["n_masks_mwe"][ind-adjust_mwe] if "n_masks_mwe" in pred_per_task else "_")
                    except:
                        pdb.set_trace()
                    #normalize = "Norm={}|".format(pred_sent["normalize"][ind]) if "normalize" in pred_per_task else "_"
                    types = pred_sent["parsing_types"][ind] if "parsing_types" in pred_per_task else "_"
                    heads = pred_sent["parsing_heads"][ind] if "parsing_heads" in pred_per_task else ind - 1
                    if cp_paste:
                        normalize = "Norm={}|".format(original_token)
                    norm_file.write("{index}\t{original}\t_\t{pos}\t_\t_\t{dep}\t_\t{types}\t{norm}\n".format(index=ind, original=original_token, pos=pos, types=types, dep=heads, norm=tenth_col))
                    original.write("{}\t{}\t_\t_\t_\t_\t_\t_\t{}\t_\n".format(ind, original_token, ind-1))
                    if cut_sent:
                        if ind > 50:
                            break
                        print("CUTTING SENT index {}>50 ".format(ind))
                norm_file.write("\n")
                original.write("\n")
        printing("WRITING predicted batch of {} original and {} normalized", var=[dir_original, dir_pred], verbose=verbose, verbose_level="raw_data")
    assert max_len_word is not None, "ERROR : something went wrong in the writer"
    return max_len_word
