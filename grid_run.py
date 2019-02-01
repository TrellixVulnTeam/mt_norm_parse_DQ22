from training.train import train
from io_.info_print import printing
import os
from evaluate.evaluate_epoch import evaluate
import numpy as np
import torch
from env.project_variables import PROJECT_PATH, TRAINING, DEV, TEST, CHECKPOINT_DIR, DEMO, DEMO2, REPO_DATASET, LIU, LEX_TRAIN, LEX_TEST, SEED_NP, SEED_TORCH, LEX_LIU_TRAIN
from uuid import uuid4

np.random.seed(SEED_NP+1)
torch.manual_seed(SEED_TORCH)


def train_eval(train_path, dev_path, model_id_pref, n_epochs=11,test_path=None,
               overall_report_dir=CHECKPOINT_DIR, overall_label="DEFAULT",get_batch_mode_all=True,
               warmup=False, args={}, use_gpu=None, freq_checkpointing=1,debug=False,compute_scoring_curve=False,
               compute_mean_score_per_sent=False,print_raw=False,freq_scoring=5,bucketing_train=True,freq_writer=None,
               extend_n_batch=1, score_to_compute_ls=None,
               verbose=0):

    hidden_size_encoder = args.get("hidden_size_encoder", 10)
    output_dim = args.get("output_dim", 10)
    char_embedding_dim = args.get("char_embedding_dim", 10)
    hidden_size_sent_encoder = args.get("hidden_size_sent_encoder", 10)
    hidden_size_decoder = args.get("hidden_size_decoder", 10)
    batch_size = args.get("batch_size", 2)
    dropout_sent_encoder, dropout_word_encoder, dropout_word_decoder = args.get("dropout_sent_encoder",0), \
    args.get("dropout_word_encoder", 0), args.get("dropout_word_decoder",0)
    n_layers_word_encoder = args.get("n_layers_word_encoder",1)
    dir_sent_encoder = args.get("dir_sent_encoder", 1)

    drop_out_word_encoder_out = args.get("drop_out_word_encoder_out", 0)
    drop_out_sent_encoder_out = args.get("drop_out_sent_encoder_out", 0)
    dropout_bridge = args.get("dropout_bridge", 0)

    word_recurrent_cell_encoder = args.get("word_recurrent_cell_encoder", "GRU")
    word_recurrent_cell_decoder = args.get("word_recurrent_cell_decoder", "GRU")
    dense_dim_auxilliary = args.get("dense_dim_auxilliary", None)
    dense_dim_auxilliary_2 = args.get("dense_dim_auxilliary_2", None)


    drop_out_char_embedding_decoder = args.get("drop_out_char_embedding_decoder", 0)
    unrolling_word= args.get("unrolling_word", False)

    auxilliary_task_norm_not_norm = args.get("auxilliary_task_norm_not_norm",False)
    char_src_attention = args.get("char_src_attention",False)
    weight_binary_loss = args.get("weight_binary_loss")
    dir_word_encoder = args.get("dir_word_encoder", 1)
    shared_context = args.get("shared_context", "all")

    schedule_training_policy = args.get("policy", None)
    learning_rate = args.get("learning_rate", 0.001)
    clipping = args.get("clipping", None)

    teacher_force = args.get("teacher_force", True)

    n_epochs = 1 if warmup else n_epochs

    if warmup:
        printing("Warm up : running 1 epoch ", verbose=verbose, verbose_level=0)
    printing("START TRAINING ", verbose_level=0, verbose=verbose)
    model_full_name = train(train_path, dev_path,
                            auxilliary_task_norm_not_norm=auxilliary_task_norm_not_norm,
                            dense_dim_auxilliary=dense_dim_auxilliary, dense_dim_auxilliary_2=dense_dim_auxilliary_2,
                            lr=learning_rate,extend_n_batch=extend_n_batch,
                            n_epochs=n_epochs, normalization=True,get_batch_mode_all=get_batch_mode_all,
                            batch_size=batch_size, model_specific_dictionary=True,freq_writer=freq_writer,
                            dict_path=None, model_dir=None, add_start_char=1,freq_scoring=freq_scoring,
                            add_end_char=1, use_gpu=use_gpu, dir_sent_encoder=dir_sent_encoder,
                            dropout_sent_encoder_cell=dropout_sent_encoder,
                            dropout_word_encoder_cell=dropout_word_encoder,
                            dropout_word_decoder_cell=dropout_word_decoder,
                            policy=schedule_training_policy,
                            dir_word_encoder=dir_word_encoder,compute_mean_score_per_sent=compute_mean_score_per_sent,
                            overall_label=overall_label,overall_report_dir=overall_report_dir,
                            label_train=REPO_DATASET[train_path], label_dev=REPO_DATASET[dev_path],
                            word_recurrent_cell_encoder=word_recurrent_cell_encoder, word_recurrent_cell_decoder=word_recurrent_cell_decoder,
                            drop_out_sent_encoder_out=drop_out_sent_encoder_out,drop_out_char_embedding_decoder=drop_out_char_embedding_decoder,
                            drop_out_word_encoder_out=drop_out_word_encoder_out, dropout_bridge=dropout_bridge,
                            freq_checkpointing=freq_checkpointing, reload=False, model_id_pref=model_id_pref,
                            score_to_compute_ls=score_to_compute_ls, mode_norm_ls=["all", "NEED_NORM", "NORMED"],
                            hidden_size_encoder=hidden_size_encoder, output_dim=output_dim,
                            char_embedding_dim=char_embedding_dim,
                            hidden_size_sent_encoder=hidden_size_sent_encoder, hidden_size_decoder=hidden_size_decoder,
                            n_layers_word_encoder=n_layers_word_encoder, compute_scoring_curve=compute_scoring_curve,
                            verbose=verbose,
                            unrolling_word=unrolling_word, char_src_attention=char_src_attention,
                            print_raw=print_raw, debug=debug,
                            shared_context=shared_context,
                            bucketing=bucketing_train, weight_binary_loss=weight_binary_loss,
                            teacher_force=teacher_force,
                            clipping=clipping,
                            checkpointing=True)

    model_dir = os.path.join(CHECKPOINT_DIR, model_full_name+"-folder")
    if test_path is not None:
      dict_path = os.path.join(CHECKPOINT_DIR, model_full_name+"-folder", "dictionaries")
      printing("START EVALUATION FINAL ", verbose_level=0, verbose=verbose)
      eval_data_paths = [DEMO]
      #eval_data_paths.append(test_path)
      import time
      start_eval = time.time()
      for get_batch_mode_evaluate in [False]:
        for eval_data in eval_data_paths:
                eval_label = REPO_DATASET[eval_data]
                evaluate(model_full_name=model_full_name, data_path=eval_data,
                         dict_path=dict_path, use_gpu=None,
                         label_report=eval_label, overall_label=overall_label+"-last+bucket_False_eval-get_batch_"+str(get_batch_mode_evaluate),
                         score_to_compute_ls=score_to_compute_ls, mode_norm_ls=["all", "NEED_NORM", "NORMED"],
                         normalization=True, print_raw=print_raw,
                         model_specific_dictionary=True, get_batch_mode_evaluate=get_batch_mode_evaluate, bucket=False,
                         compute_mean_score_per_sent=compute_mean_score_per_sent,
                         batch_size=50,debug=debug,
                         dir_report=model_dir, verbose=1)
    print("END EVAL", time.time()-start_eval)
    return model_full_name, model_dir

#4538


if __name__ == "__main__":

      ##train_path = LIU
      ##dev_path = DEV
      params = []

      ls_param = ["hidden_size_encoder", "hidden_size_sent_encoder","hidden_size_decoder", "output_dim", "char_embedding_dim"]
      param_0 = {"hidden_size_encoder": 5, "output_dim": 10, "char_embedding_dim": 10,
                 "dropout_sent_encoder": 0., "dropout_word_encoder": 0., "dropout_word_decoder": 0.,
                 "n_layers_word_encoder": 1, "dir_sent_encoder": 2,
                 "hidden_size_sent_encoder": 10, "hidden_size_decoder": 5, "batch_size": 10}

      params_baseline = {"hidden_size_encoder": 50, "output_dim": 100, "char_embedding_dim": 50,
                         "dropout_sent_encoder": 0., "drop_out_word_encoder": 0., "dropout_word_decoder": 0.,
                         "drop_out_sent_encoder_out": 1, "drop_out_word_encoder_out": 1, "dir_word_encoder": 1,
                         "n_layers_word_encoder": 1, "dir_sent_encoder": 1, "word_recurrent_cell_decoder": "LSTM", "word_recurrent_cell_encoder":"LSTM",
                         "hidden_size_sent_encoder": 50, "hidden_size_decoder": 50, "batch_size": 10}
      params_intuition = {"hidden_size_encoder": 40, "output_dim": 50, "char_embedding_dim": 30,
                         "dropout_sent_encoder": 0., "drop_out_word_encoder": 0., "dropout_word_decoder": 0.,
                         "drop_out_sent_encoder_out": 0, "drop_out_word_encoder_out": 0, "dir_word_encoder": 1,
                         "n_layers_word_encoder": 1, "dir_sent_encoder": 1, "word_recurrent_cell_decoder": "LSTM",
                         "word_recurrent_cell_encoder": "LSTM",
                         "hidden_size_sent_encoder": 15, "hidden_size_decoder": 40, "batch_size": 10}
      params_strong = {"hidden_size_encoder": 200, "output_dim": 100, "char_embedding_dim": 50,
                         "dropout_sent_encoder": 0, "drop_out_word_encoder": 0, "dropout_word_decoder": 0.,
                         "drop_out_word_encoder_out": 0.3, "drop_out_sent_encoder_out": 0.3, "drop_out_char_embedding_decoder":0.3, "dropout_bridge":0.01,
                         "n_layers_word_encoder": 1, "dir_sent_encoder": 1,"word_recurrent_cell_decoder": "LSTM", "word_recurrent_cell_encoder":"LSTM",
                         "hidden_size_sent_encoder": 100, "hidden_size_decoder": 200, "batch_size": 10}

      label_0 = "origin_small-batch10-LSTM_sent_bi_dir-word_uni_LSTM"

      ABLATION_NETWORK_SIZE = False

      if ABLATION_NETWORK_SIZE:
          params = [param_0]
          labels = [label_0]
          for level in [2,4,8,16]:
            for _, arg in enumerate(ls_param):
              param = {}
              param[arg] = param_0[arg]*2 if param_0[arg]*2<=100 else 100
            labels.append(str(level)+"-level-"+label_0[12:])
            params.append(param)
      i = 0

      ABLATION_DROPOUT = False

      if ABLATION_DROPOUT:
          params = []
          labels = [""]
          for add_dropout_encoder in [0,0.1,0.2,0.5,0.8]:
            for batch_size in [10, 20, 50, 100]:
              for dir_sent_encoder in [1, 2]:
                param = params_baseline.copy()
                param["drop_out_sent_encoder_out"] = 0.2#add_dropout_encoder
                param["drop_out_word_encoder_out"] = 0.2#add_dropout_encoder
                param["dropout_bridge"] = 0.2#add_dropout_encoder
                param["drop_out_char_embedding_decoder"] = add_dropout_encoder
                param["dir_sent_encoder"] = dir_sent_encoder
                param["batch_size"] = batch_size

                label = str(add_dropout_encoder)+"-to_char_src-"+str(dir_sent_encoder)+"_dir_sent-"+str(batch_size)+"_batch_size"
                params.append(param)
                labels.append(label)

      ABLATION_DIR_WORD = False

      if ABLATION_DIR_WORD:
          params = [params_strong]
          labels = ["dir_word_encoder_1-strong-sent_source_dir_2-dropout_0.2_everywhere-LSTM-batch_10"]
          param = params_strong.copy()
          param["dir_word_encoder"] = 2
          param["hidden_size_encoder"] = int(param["hidden_size_encoder"]/2)
          params.append(param)
          labels.append("dir_word_encoder_2-sent_source_dir_2-dropout_0.2_everywhere-LSTM-batch_10")

      WITH_AUX = False
      if WITH_AUX:
          params = []
          labels = []
          n_model = 0
          for dense_dim_auxilliary in [None, 200, 400]:
              policy_ls = ["policy_2", None] if dense_dim_auxilliary is not None else [None]
              auxilliary_task_norm_not_norm = False if dense_dim_auxilliary is None else True
              for policy in policy_ls:
              #for weight_binary_loss in [0.001,1,10,100]:
                #auxilliary_task_norm_not_norm = False if dense_dim_auxilliary else True
                weight_binary_loss_ls = [0] if not auxilliary_task_norm_not_norm else [0.05, 0.025]
                for dir_word_encoder in [1]:
                  for weight_binary_loss in weight_binary_loss_ls:
                      for drop_out_char_embedding_decoder in [0.2]:
                          for char_src_attention in [False]:
                            for unrolling_word in [True]:
                              if char_src_attention == True and unrolling_word==False:
                                continue
                              i += 1
                              param = params_strong.copy()
                              param["drop_out_sent_encoder_out"] = 0.0#add_dropout_encoder
                              param["drop_out_word_encoder_out"] = 0.0#add_dropout_encoder
                              param["dropout_bridge"] = 0.1 #add_dropout_encoder
                              param["drop_out_char_embedding_decoder"] = drop_out_char_embedding_decoder
                              param["dir_word_encoder"] = dir_word_encoder
                              param["dir_sent_encoder"] = 1
                              param["batch_size"] = 25
                              param["char_src_attention"] = char_src_attention
                              param["dense_dim_auxilliary"] = dense_dim_auxilliary
                              param["unrolling_word"] = unrolling_word
                              param["auxilliary_task_norm_not_norm"] = auxilliary_task_norm_not_norm
                              param["shared_context"] = "all"
                              param["weight_binary_loss"] = weight_binary_loss
                              param["policy"] = policy
                              param["clipping"] = 1
                              #label = str(dense_dim_auxilliary)+"-dense_dim_auxilliary"
                              label = str(dir_word_encoder)+"dir_word-" +str(dense_dim_auxilliary)+"_aux-"+str(drop_out_char_embedding_decoder)+"do_char_dec-"+str(char_src_attention)+"_char_src"
                                      #"dense_bin"+str(param["drop_out_word_encoder_out"])+"-do_char-" +\
                                      #str(param["dir_sent_encoder"])+"_dir_sent-"+str(param["batch_size"])+"_batch" + "-dir_word_src_" +\
                                      #str(param["dir_word_encoder"])+"-unrolling_word_"+str(unrolling_word)+
                              params.append(param)
                              #labels.append("model_"+str(n_model))
                              labels.append(label)

      FROM_BEST = True
      if FROM_BEST:
          params = []
          labels = []
          n_model = 0
          for batch_size in [10, 50]:
            for scale in [2, 5]:
              for clipping in [1]:
                for dir_word_encoder in [2, 1]:
                    for teacher_force in [True]:
                      param = params_intuition.copy()
                      param["hidden_size_encoder"] *=scale
                      param["hidden_size_sent_encoder"]*=scale
                      param["hidden_size_decoder"]*=scale
                      param["output_dim"] *= int(scale*0.5)+1
                      param["batch_size"] = batch_size
                      param["unrolling_word"] = True
                      param["dir_word_encoder"] = dir_word_encoder
                      param["dir_sent_encoder"] = 1
                      param["teacher_force"] = teacher_force
                      params.append(param)
                      labels.append("best-scale-{}-{}-{}dir_word_encoder-all_context-no_aux-no_att-no_dropout".format(scale,batch_size, dir_word_encoder))

      warmup = True
      test_before_run = False

      RUN_ID = str(uuid4())[0:5]
      
      LABEL_GRID = "best-dim_word_fixed" if not warmup else "WARMUP-unrolling-False"
      LABEL_GRID = "test_before_run-"+LABEL_GRID if test_before_run else LABEL_GRID

      OAR = os.environ.get('OAR_JOB_ID')+"_rioc-" if os.environ.get('OAR_JOB_ID', None) is not None else ""
      LABEL_GRID = OAR+RUN_ID+"-"+LABEL_GRID

      GRID_FOLDER_NAME = LABEL_GRID if len(LABEL_GRID) > 0 else RUN_ID
      GRID_FOLDER_NAME += "-summary"
      dir_grid = os.path.join(CHECKPOINT_DIR, GRID_FOLDER_NAME)
      os.mkdir(dir_grid)
      printing("INFO : dir_grid {} made".format(dir_grid), verbose=0, verbose_level=0)
      train_path, dev_path = LIU, DEV
      for param, model_id_pref in zip(params, labels):
          i += 1
          printing("Adding RUN_ID {} as prefix".format(RUN_ID), verbose=0, verbose_level=0)
          epochs = 80 if not test_before_run else 20
          if warmup:
            param = {"hidden_size_encoder": 10, "output_dim": 15, "char_embedding_dim": 10,
                     "dropout_sent_encoder": 0., "drop_out_word_encoder": 0., "dropout_word_decoder": 0.,
                     "drop_out_sent_encoder_out": 0, "drop_out_word_encoder_out": 0,
                     "dir_word_encoder": 1,
                     "n_layers_word_encoder": 1, "dir_sent_encoder": 1, "word_recurrent_cell_decoder": "LSTM",
                     "word_recurrent_cell_encoder": "LSTM",
                     "hidden_size_sent_encoder": 20, "hidden_size_decoder": 30, "batch_size": 10}
            param["batch_size"] = 50
            param["auxilliary_task_norm_not_norm"] = True
            param["weight_binary_loss"] = 0.05
            param["unrolling_word"] = True
            param["char_src_attention"] = False
            train_path, dev_path = DEMO2, DEMO
            param["shared_context"] = "word"
            param["dense_dim_auxilliary"] = 0
            param["clipping"] = None
            param["teacher_force"] = False
            param["dense_dim_auxilliary_2"] = 50

          model_id_pref = LABEL_GRID + model_id_pref + "-model_"+str(i)
          print("GRID RUN : MODEL {} with param {} ".format(model_id_pref, param))
          model_full_name, model_dir = train_eval(train_path, dev_path, model_id_pref,
                                                  test_path=DEV,
                                                  verbose=1,
                                                  overall_report_dir=dir_grid, overall_label=LABEL_GRID,
                                                  compute_mean_score_per_sent=True, print_raw=False,
                                                  get_batch_mode_all=True, compute_scoring_curve=False,
                                                  freq_scoring=1, bucketing_train=True, freq_checkpointing=1,
                                                  freq_writer=10 if not test_before_run else 1,
                                                  extend_n_batch=2,
                                                  score_to_compute_ls=["exact", "norm_not_norm-F1",
                                                                       "norm_not_norm-Precision",
                                                                       "norm_not_norm-Recall",
                                                                       "norm_not_norm-accuracy"],
                                                  warmup=warmup, args=param, use_gpu=None, n_epochs=epochs,
                                                  debug=True)
          run_dir = os.path.join(dir_grid, RUN_ID+"-run-log")
          open(run_dir, "a").write("model : done "+model_full_name+" in "+model_dir+" \n")
          print("Log RUN is : {} to see model list ".format(run_dir))
          print("GRID RUN : DONE MODEL {} with param {} ".format(model_id_pref, param))

          if warmup :
            break

# CCL want to have a specific seed : when work --> reproduce with several seed