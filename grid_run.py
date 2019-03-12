
from io_.info_print import printing
import os

from training.train_eval import train_eval
from training.fine_tune import fine_tune
from toolbox.grid_tool import grid_param_label_generate
from env.project_variables import PROJECT_PATH, TRAINING,LIU_TRAIN, DEMO_SENT, CP_WR_PASTE_TEST_269, \
    LIU_DEV, DEV, DIR_TWEET_W2V, TEST, DIR_TWEET_W2V, CHECKPOINT_DIR, DEMO, DEMO2, CP_PASTE_WR_TRAIN, \
    CP_WR_PASTE_DEV, CP_WR_PASTE_TEST, CP_PASTE_DEV, CP_PASTE_TRAIN, CP_PASTE_TEST, EWT_DEV, EWT_TEST, \
    LIU_DEV_SENT, LIU_TRAIN_SENT, DEV_SENT, TEST_SENT, DEMO_SENT, TRAINING_DEMO, EN_LINES_EWT_TRAIN, EN_LINES_DEV, EN_LINES_EWT_TRAIN, \
    MTNT_TOK_TRAIN, MTNT_TOK_DEV, MTNT_EN_FR_TRAIN, MTNT_EN_FR_DEV, MTNT_EN_FR_TEST, RUN_SCRIPTS_DIR, GPU_AVAILABLE_DEFAULT_LS
from uuid import uuid4
import argparse
from sys import platform
from toolbox.git_related import get_commit_id
from tracking.reporting_google_sheet import update_status, append_reporting_sheet
from toolbox.grid_script_generation import script_generation

FINE_TUNE = 0
GRID = 1


def run_grid(params, labels, dir_grid, label_grid, train_path, dev_path, test_paths, epochs=50, test_before_run=False, warmup=False):
    i = 0
    for param, model_id_pref in zip(params, labels):
        i += 1
        printing("GRID RUN : RUN_ID {} as prefix".format(RUN_ID), verbose=0, verbose_level=0)
        epochs = epochs if not test_before_run else 1
        if warmup:
            train_path, dev_path = DEMO, DEMO2
            param["word_embed_init"] = None

        model_id_pref = label_grid + model_id_pref + "-model_" + str(i)
        if warmup:
            epochs = 1
            print("GRID RUN : MODEL {} with param {} ".format(model_id_pref, param))
            print("GRID_INFO analy vars=    dense_dim_auxilliary_pos_2 dense_dim_auxilliary_pos")
            print("GRID_INFO fixed vars=  word_embed ")
            print("GRID_INFO fixed vals=  word_embed,False ")

        model_full_name, model_dir = train_eval(train_path, dev_path, model_id_pref,
                                                expand_vocab_dev_test=True,
                                                test_path=test_paths if not warmup else DEMO,
                                                overall_report_dir=dir_grid, overall_label=LABEL_GRID,
                                                compute_mean_score_per_sent=True, print_raw=False,
                                                get_batch_mode_all=True, compute_scoring_curve=False,
                                                freq_scoring=10, bucketing_train=True, freq_checkpointing=1,
                                                symbolic_root=True, symbolic_end=True,
                                                freq_writer=1 if not test_before_run else 1,
                                                extend_n_batch=2,
                                                score_to_compute_ls=["exact", "norm_not_norm-F1",
                                                                     "norm_not_norm-Precision",
                                                                     "norm_not_norm-Recall",
                                                                     "norm_not_norm-accuracy"],
                                                warmup=warmup, args=param, use_gpu=None, n_epochs=epochs,
                                                debug=False,
                                                verbose=1)

        run_dir = os.path.join(dir_grid, RUN_ID + "-run-log")
        open(run_dir, "a").write("model : done " + model_full_name + " in " + model_dir + " \n")
        print("GRID : Log RUN is : {} to see model list ".format(run_dir))
        print("GRID RUN : DONE MODEL {} with param {} ".format(model_id_pref, param))
        if warmup:
            break


if __name__ == "__main__":

      if platform != "darwin":
        printing("RUN : running in rioc", verbose=1, verbose_level=1)
        assert os.environ.get("MODE_RUN") is not None, "Running in rioc, MODE_RUN empty while it should not "
        assert os.environ.get("MODE_RUN") in ["DISTRIBUTED", "SINGLE"]
        run_standart = os.environ.get("MODE_RUN") != "DISTRIBUTED"
      else:
          run_standart = False


      params = []

      ls_param = ["hidden_size_encoder", "hidden_size_sent_encoder","hidden_size_decoder", "output_dim", "char_embedding_dim"]
      params_strong = {"hidden_size_encoder": 100, "output_dim": 100, "char_embedding_dim": 50,
                         "dropout_sent_encoder": 0.3, "drop_out_word_encoder": 0.3, "dropout_word_decoder": 0.,
                         "drop_out_word_encoder_out": 0.3, "drop_out_sent_encoder_out": 0.3, "drop_out_char_embedding_decoder":0.3, "dropout_bridge":0.01,
                         "n_layers_word_encoder": 1, "dir_sent_encoder": 2,"word_recurrent_cell_decoder": "LSTM", "word_recurrent_cell_encoder":"LSTM",
                         "hidden_size_sent_encoder": 100, "hidden_size_decoder": 200, "batch_size": 10}

      params_strong_tryal = {"hidden_size_encoder": 20, "output_dim": 20, "char_embedding_dim": 40,
                            "dropout_sent_encoder": 0, "drop_out_word_encoder": 0, "dropout_word_decoder": 0.,
                            "drop_out_word_encoder_out": 0., "drop_out_sent_encoder_out": 0.,
                            "drop_out_char_embedding_decoder": 0., "dropout_bridge": 0.0,
                            "n_layers_word_encoder": 1, "dir_sent_encoder": 2, "word_recurrent_cell_decoder": "LSTM",
                            "word_recurrent_cell_encoder": "LSTM",
                            "hidden_size_sent_encoder": 24, "hidden_size_decoder": 30, "batch_size": 10}
      params_dozat = {"hidden_size_encoder": 200, "output_dim": 100, "char_embedding_dim": 100,
                        "dropout_sent_encoder": 0.5, "drop_out_word_encoder": 0.5, "dropout_word_decoder": 0.3,
                        "drop_out_word_encoder_out": 0.5, "drop_out_sent_encoder_out": 0.0,
                        "drop_out_char_embedding_decoder": 0.1, "dropout_bridge": 0.5,
                        "n_layers_word_encoder": 1, "dir_sent_encoder": 2, "word_recurrent_cell_decoder": "LSTM",
                        "word_recurrent_cell_encoder": "LSTM",
                        "hidden_size_sent_encoder": 200, "hidden_size_decoder": 100, "batch_size": 500}

      grid_label = "B"#"POS-2LSMT-2dense+no_aux_task-sent_only-EWT_DEV-PONDERATION-1pos-0_norm"
      # param["policy"] = policy
      # param["drop_out_sent_encoder_out"] = 0.2#add_dropout_encoder
      # param["drop_out_word_encoder_out"] = 0.2#add_dropout_encoder
      # param["dropout_bridge"] = 0.2 #add_dropout_encoder
      # param["drop_out_char_embedding_decoder"] = add_dropout_encoder
      # param["dense_dim_auxilliary"] = dense_dim_auxilliary
      # param["dense_dim_auxilliary_2"] = dense_dim_auxilliary_2
      # param["dense_dim_word_pred"] = 200 if word_decoding else None
      # param["dense_dim_word_pred_2"] = 200 if word_decoding else None
      # param["dense_dim_word_pred_3"] = 100 if word_decoding else None
      # param["dense_dim_auxilliary_pos"] = None if not auxilliary_task_pos else 200
      # param["dense_dim_auxilliary_pos_2"] = None

      if run_standart:
          # default not used but could be
          params, labels, default_all, analysed, fixed = grid_param_label_generate(
                                                                                  params_strong,
                                                                                  warmup=False,
                                                                                  grid_label="0",
                                                                                  stable_decoding_state_ls=[False],
                                                                                  word_decoding_ls=[False],
                                                                                  batch_size_ls=[50, 100,200,400],
                                                                                  #auxilliary_task_pos_ls=[False],
                                                                                  word_embed_ls=[False],
                                                                                  dir_sent_encoder_ls=[2], lr_ls=[0.0001,0.001,0.05],
                                                                                  word_embed_init_ls=[None],
                                                                                  teacher_force_ls=[True],
                                                                                  proportion_pred_train_ls=[None],
                                                                                  shared_context_ls=["all"],
                                                                                  word_embedding_projected_dim_ls=[None],
                                                                                  #auxilliary_task_norm_not_norm_ls=[True],
                                                                                  tasks_ls=[["normalize"]],
                                                                                  char_src_attention_ls=[True],
                                                                                  n_layers_sent_cell_ls=[2],
                                                                                  unrolling_word_ls=[True],
                                                                                  scale_ls=[2]
                                                                                  )



          # only for cloud run :

      warmup = True
      if platform != "darwin":
          printing("ENV : running not from os x assuming we are in command shell run", verbose=0, verbose_level=0)
          parser = argparse.ArgumentParser()
          parser.add_argument("--test_before_run", help="test_before_run", action="store_true")
          args = parser.parse_args()
          test_before_run = args.test_before_run
          print("GRID : test_before_run set to {} ".format(test_before_run))
          warmup = False
          environment = "rioc"
          OAR = os.environ.get('OAR_JOB_ID') + "_rioc-" if os.environ.get('OAR_JOB_ID', None) is not None else ""
          print("OAR=", OAR)
          log = "{}/logs/{}".format(os.getcwd(), os.environ.get('OAR_JOB_ID')+"-job.stdout")
      else:
          OAR=""
          environment = "local"
          log = "in the fly logs"
          test_before_run = False

      RUN_ID = str(uuid4())[0:5]
      LABEL_GRID = grid_label if not warmup else "WARMUP-unrolling-False"
      LABEL_GRID = "test_before_run-"+LABEL_GRID if test_before_run else LABEL_GRID
      OAR = RUN_ID if OAR == "" else OAR
      LABEL_GRID = OAR+"-"+LABEL_GRID
      GRID_FOLDER_NAME = LABEL_GRID if len(LABEL_GRID) > 0 else RUN_ID
      GRID_FOLDER_NAME += "-summary"
      dir_grid = os.path.join(CHECKPOINT_DIR, GRID_FOLDER_NAME)
      os.mkdir(dir_grid)
      printing("GRID RUN : Grid directory : dir_grid {} made".format(dir_grid), verbose=0, verbose_level=0)

      if run_standart:
          try:
              n_models = len(params) if not warmup else 1
              warmup_desc = "warmup" if warmup else ""
              test_before_run_desc = "test_before_run" if test_before_run else ""
              description = "{} models : Analysing : {} with regard to {} fixed".format(n_models, to_analysed,
                                                                                        to_keep_only)
              row, col = append_reporting_sheet(git_id=get_commit_id(), rioc_job=LABEL_GRID, description=description,
                                                log_dir=log, target_dir=dir_grid + " | " + os.path.join(CHECKPOINT_DIR,
                                                                                                        "{}*".format(
                                                                                                            LABEL_GRID)),
                                                env=environment, status="running {}{}".format(warmup_desc,test_before_run_desc),
                                                verbose=1)
              train_path, dev_path = MTNT_TOK_TRAIN, MTNT_TOK_DEV  #EN_LINES_EWT_TRAIN, EWT_DEV  # MTNT_TOK_TRAIN, MTNT_TOK_DEV#EN_LINES_EWT_TRAIN, EWT_DEV # MTNT_EN_FR_TRAIN, MTNT_EN_FR_DEV #MTNT_TOK_TRAIN, MTNT_TOK_DEV#EN_LINES_EWT_TRAIN, EWT_DEV#CP_PASTE_WR_TRAIN, CP_WR_PASTE_DEV#TRAINING, EWT_DEV #LIU_TRAIN, LIU_DEV ## EWT_DEV, DEV
              run_grid(params=params, labels=labels, dir_grid=dir_grid, label_grid=LABEL_GRID,
                       epochs=5,test_before_run=test_before_run,
                       train_path=train_path,
                       dev_path=dev_path,
                       test_paths=[TEST_SENT, MTNT_EN_FR_TEST, MTNT_EN_FR_DEV],#[EWT_TEST, EWT_DEV, EN_LINES_EWT_TRAIN, TEST], # [TEST_SENT, MTNT_EN_FR_TEST, MTNT_EN_FR_DEV],#
                       warmup=warmup)
              update_status(row=row, new_status="done {}".format(warmup_desc), verbose=1)
          except Exception as e:
              update_status(row=row, new_status="failed {} (error {})".format(warmup_desc, e), verbose=1)
              raise(e)


      else:
          epochs=1
          train_path, dev_path = EN_LINES_EWT_TRAIN, EWT_DEV  # MTNT_TOK_TRAIN, MTNT_TOK_DEV#EN_LINES_EWT_TRAIN, EWT_DEV # MTNT_EN_FR_TRAIN, MTNT_EN_FR_DEV #MTNT_TOK_TRAIN, MTNT_TOK_DEV#EN_LINES_EWT_TRAIN, EWT_DEV#CP_PASTE_WR_TRAIN, CP_WR_PASTE_DEV#TRAINING, EWT_DEV #LIU_TRAIN, LIU_DEV ## EWT_DEV, DEV
          dir_script, row = script_generation(grid_label=LABEL_GRID, init_param=params_dozat, warmup=test_before_run,
                                              dir_grid=dir_grid, environment=environment, dir_log=log,
                                              stable_decoding_state_ls=[False],
                                              word_decoding_ls=[False],
                                              epochs=epochs,
                                              batch_size_ls=[50, 100, 200, 400],
                                              word_embed_ls=[False],
                                              dir_sent_encoder_ls=[2], lr_ls=[0],
                                              word_embed_init_ls=[None],
                                              teacher_force_ls=[True],
                                              proportion_pred_train_ls=[None],
                                              shared_context_ls=["all"],
                                              word_embedding_projected_dim_ls=[None],
                                              tasks_ls=[["pos"]],
                                              char_src_attention_ls=[True],
                                              n_layers_sent_cell_ls=[2],
                                              unrolling_word_ls=[True],
                                              scale_ls=[1],
                                              overall_report_dir=dir_grid, overall_label=LABEL_GRID,
                                              train_path=DEV, dev_path=TEST, test_paths=[DEV, EWT_DEV,TEST], gpu_mode="random",
                                              gpus_ls=GPU_AVAILABLE_DEFAULT_LS,
                                              write_to_dir=RUN_SCRIPTS_DIR)
          print("row:{}".format(row))
          print("dir_script:{}".format(dir_script))


# WARNING : different behavior in warmup and test_before_run between DISTRIBUTED mode and SINGLE mode
## in SINGLE mode only warmup means one mode train and evaluated in the grid search for 1 epoch
    #  test_before models all models are run and evaluation
## in DISTRIBUTED : they are merged and corresponds to test_before_run

# oarsub -q gpu
# -l /core=2,walltime=48:00:00
# -p "host='gpu004'" -O ./logs/%jobid%-job.stdout -E ./logs/%jobid%-job.stderr ./train/train_mt_norm.sh
