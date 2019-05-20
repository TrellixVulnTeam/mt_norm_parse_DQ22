import os
# SEEDS
SEED_NP = 123
SEED_TORCH = 123

# ENVIRONMENT VARIABLES
PROJECT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
RUN_SCRIPTS_DIR = os.path.join(PROJECT_PATH, "run_scripts")
LM_PROJECT = os.path.join(PROJECT_PATH, "..", "representation", "lm")

# MODELS
# checkpoint dir if not checkpoint_dir as defined in args.json not found
CHECKPOINT_DIR = os.path.join(PROJECT_PATH, "checkpoints")
# SPECIFIC LCATION FOR BERT CHECKPOINT
CHECKPOINT_BERT_DIR = os.path.join(PROJECT_PATH, "checkpoints", "bert")

assert os.path.isdir(CHECKPOINT_BERT_DIR ), "ERROR : {} CHECKPOINT_BERT_DIR  does not exist  ".format(CHECKPOINT_BERT_DIR)

CLIENT_GOOGLE_CLOUD = os.path.join(PROJECT_PATH, "tracking/google_api")
SHEET_NAME_DEFAULT, TAB_NAME_DEFAULT = "model_evaluation", "experiments_tracking"

LIST_ARGS = ["tasks", "train_path", "dev_path", "test_path", "heuristic_ls", "masking_strategy"]
NONE_ARGS = ["gpu"]
BOOL_ARGS = ["word_embed", "teacher_force", "char_decoding", "unrolling_word", "init_context_decoder",
             "word_decoding", "stable_decoding_state", "char_src_attention"]
DIC_ARGS = ["multi_task_loss_ponderation", "lr"]
GPU_AVAILABLE_DEFAULT_LS = ["0", "1", "2", "3"]

# architecture/model/training supported
SUPPORED_WORD_ENCODER = ["LSTM", "GRU", "WeightDropLSTM"]
BREAKING_NO_DECREASE = 21
STARTING_CHECKPOINTING_WITH_SCORE = 30
SUPPORTED_STAT = ["sum"]
LOSS_DETAIL_TEMPLATE = {"loss_overall": 0,
                        "loss_seq_prediction": 0, "loss_binary": 0, "loss_pos": 0, "loss_edit": 0,
                        "other": {}}
LOSS_DETAIL_TEMPLATE_LS = {"loss_overall": [], "loss_seq_prediction": [],
                           "loss_binary": [], "loss_pos": [], "loss_edit": [],
                           "other": {}}
SCORE_AUX = ["norm_not_norm-F1", "norm_not_norm-Precision", "norm_not_norm-Recall", "norm_not_norm-accuracy"]

AVAILABLE_TASKS = ["all", "normalize", "norm_not_norm", "pos", "edit_prediction"]
AVAILABLE_AGGREGATION_FUNC_AUX_TASKS = ["norm_not_norm", "edit_prediction"]
AVAILABLE_BERT_FINE_TUNING_STRATEGY = ["bert_out_first", "standart", "flexible_lr", "only_first_and_last"]
AVAILABLE_BERT_MASKING_STRATEGY = ["normed", "cls", "start_stop"]
HEURISTICS = ["gold_detection", "#", "@", "url", "slang_translate", "edit_check-all", "edit_check-data", "edit_check-ref"]

TASKS_2_METRICS_STR = {"all": ["accuracy-exact-normalize", "accuracy-normalize","InV-accuracy-normalize","OOV-accuracy-normalize","npv-normalize", "recall-normalize","precision-normalize","tnr-normalize", "accuracy-exact-pos", "f1-normalize"],
                       "normalize": ["accuracy-exact-normalize", "accuracy-normalize", "npv-normalize", "recall-normalize", "precision-normalize", "tnr-normalize", "f1-normalize"],
                       "pos": ["accuracy-exact-pos"],
                       "edit_prediction": [""],
                       "norm_not_norm": ["IoU-pred-normed","recall-norm_not_norm","accuracy-norm_not_norm","IoU-pred-need_norm","precision-norm_not_norm"]}
# "InV-accuracy-normalize", "OOV-accuracy-normalize"
AVAILABLE_OPTIMIZER = ["adam", "bahdanu-adadelta", "SGD"]
MULTI_TASK_LOSS_PONDERATION_PREDEFINED_MODE = ["uniform", "normalization_100", "pos_100","all","pos", "normalize","norm_not_norm"]
DEFAULT_SCORING_FUNCTION = "exact_match"
AVAILABLE_WORD_LEVEL_LABELLING_MODE = ["word", "pos", "norm_not_norm"]



# DATASETS proportion_pred_train_ls
TRAINING_LABEL, TRAINING = "en-ud-train", os.path.join(PROJECT_PATH, "../parsing/normpar/data/en-ud-train.conllu")
TRAINING_DEMO_LABEL, TRAINING_DEMO = "en-ud-train_demo", os.path.join(PROJECT_PATH, "../parsing/normpar/data/en-ud-train_demo.conllu")

EWT_TEST_LABEL, EWT_TEST = "ewt_test", os.path.join(PROJECT_PATH, "../parsing/normpar/data/en-ud-test.conllu")

EWT_PRED_TOKEN_UDPIPE_LABEL, EWT_PRED_TOKEN_UDPIPE = "ud_pred_tokens-ewt_dev",os.path.join(PROJECT_PATH, "data", "udpipe_pred_tokens", "en_ewt-udpipe.conllu")

EWT_DEV_LABEL, EWT_DEV = "ewt_dev", os.path.join(PROJECT_PATH, "../parsing/normpar/data/en-ud-dev.integrated-po_as_norm")
DEV_LABEL, DEV = "owoputi", os.path.join(PROJECT_PATH, "../parsing/normpar/data/owoputi.integrated_fixed")
TEST_LABEL, TEST = "lexnorm", os.path.join(PROJECT_PATH, "../parsing/normpar/data/lexnorm.integrated")


DEMO_LABEL, DEMO = "lexnorm-Demo", os.path.join(PROJECT_PATH, "../parsing/normpar/data/lexnorm.integrated.demo")
DEMO2_LABEL, DEMO2 = "lexnorm-demo2", os.path.join(PROJECT_PATH, "../parsing/normpar/data/lexnorm.integrated.demo2")

LIU_LABEL, LIU = "liu_data", os.path.join(PROJECT_PATH, "./data/LiLiu/2577_tweets-li.conll")
LIU_OWOPUTI_LABEL, LIU_OWOPUTI = "liu_all+owoputi", os.path.join(PROJECT_PATH, "./data/LiLiu/2577_tweets-li-train+dev_500+owoputi_integrated_fixed.conll")
LIU_TRAIN_OWOPUTI_LABEL, LIU_TRAIN_OWOPUTI = "liu_train+owoputi", os.path.join(PROJECT_PATH, "./data/LiLiu/2577_tweets-li-train_2009-fixed+owoputi_integrated_fixed.conll")

LIU_DEV_LABEL, LIU_DEV = "liu_dev", os.path.join(PROJECT_PATH, "./data/LiLiu/2577_tweets-li-dev_500.conll")
LIU_DEV_OWOPUTI_LABEL, LIU_DEV_OWOPUTI = "liu_dev_owoputi", os.path.join(PROJECT_PATH, "./data/LiLiu/2577_tweets-li-dev_500+owoputi_integrated_fixed.conll")

LIU_TRAIN_LABEL, LIU_TRAIN = "liu_train", os.path.join(PROJECT_PATH, "./data/LiLiu/2577_tweets-li-train_2009.conll")

LIU_TRAIN_OWOPUTI_LEX_TRAIN_LABEL, LIU_TRAIN_OWOPUTI_LEX_TRAIN = "lex_norm2015_train-space_demo", os.path.join(PROJECT_PATH, "./data/LiLiu/2577_tweets-li-train_2009-fixed+owoputi_integrated_fixed+lexnorm_train.conll")
LEX_TRAIN_SPACE_DEMO_LABEL, LEX_TRAIN_SPACE_DEMO = "lex_norm2015_train-space_demo", os.path.join(PROJECT_PATH, "./data/wnut-2015-ressources/lexnorm2015/train_data-space_demo.conll")
LEX_TRAIN_LABEL, LEX_TRAIN = "lex_norm2015_train", os.path.join(PROJECT_PATH, "./data/wnut-2015-ressources/lexnorm2015/train_data.conll")

LEX_TRAIN_SPLIT_LABEL, LEX_TRAIN_SPLIT = "lex_norm2015_split_train", os.path.join(PROJECT_PATH, "./data/wnut-2015-ressources/lexnorm2015/train_split_data.conll")
LEX_DEV_SPLIT_LABEL, LEX_DEV_SPLIT = "lex_norm2015_split_dev", os.path.join(PROJECT_PATH, "./data/wnut-2015-ressources/lexnorm2015/dev_split_data.conll")

LEX_TEST_LABEL, LEX_TEST = "lex_norm2015_test", os.path.join(PROJECT_PATH, "./data/wnut-2015-ressources/lexnorm2015/test_truth.conll")

LEX_LIU_LABEL, LEX_LIU_TRAIN = "lex_train+liu", os.path.join(PROJECT_PATH, "./data/lexnorm2015/lex_norm_train+liu_2577.conll")

CP_PASTE_TRAIN_LABEL, CP_PASTE_TRAIN = "copy_paste-train", os.path.join(PROJECT_PATH, "./data/copy_paste_train.conll")
CP_PASTE_DEV_LABEL, CP_PASTE_DEV = "copy_paste-dev", os.path.join(PROJECT_PATH, "./data/copy_paste_dev.conll")
CP_PASTE_TEST_LABEL, CP_PASTE_TEST = "copy_paste-test", os.path.join(PROJECT_PATH, "./data/copy_paste_test.conll")

CP_PASTE_WR_TRAIN_LABEL, CP_PASTE_WR_TRAIN = "copy_paste_real_word-train", os.path.join(PROJECT_PATH, "./data/copy_paste_real_word_train.conll")
CP_PASTE_WR_DEV_LABEL, CP_WR_PASTE_DEV = "copy_paste_real_word-dev", os.path.join(PROJECT_PATH, "./data/copy_paste_real_word_dev.conll")
CP_PASTE_WR_TEST_LABEL, CP_WR_PASTE_TEST = "copy_paste_real_word-test", os.path.join(PROJECT_PATH, "./data/copy_paste_real_word_test.conll")

CP_PASTE_WR_TEST_269_LABEL, CP_WR_PASTE_TEST_269 = "copy_paste_real_word_test-first269", os.path.join(PROJECT_PATH, "./data/copy_paste_real_word_test-first269.conll")

# AUGME

DIR_TWEET_W2V = os.path.join(PROJECT_PATH, "w2v", "tweets.en.w2v.txt")
DIR_FASTEXT_WIKI_NEWS_W2V = os.path.join(PROJECT_PATH, "w2v", "wiki-news-300d-1M.vec")
FASTEXT_WIKI_NEWS_W2V_LABEL = "wiki-news"
TWEET_W2V_LABEL = "tweets_en_w2v"


W2V_LOADED_DIM = 400
MAX_VOCABULARY_SIZE_WORD_DIC = 20000

# Michel
##
MTNT_TOK_TRAIN_LABEL, MTNT_TOK_TRAIN = "mtnt_tok_train", os.path.join(PROJECT_PATH, "./data/MTNT/monolingual/train.en.raw2tok.conll")
MTNT_TOK_DEV_LABEL, MTNT_TOK_DEV = "mtnt_tok_dev", os.path.join(PROJECT_PATH, "./data/MTNT/monolingual/dev.en.raw2tok.conll")

MTNT_EN_FR_TRAIN_LABEL, MTNT_EN_FR_TRAIN = "mtnt_train", os.path.join(PROJECT_PATH, "./data/MTNT/train/train.en-fr.conll")
MTNT_EN_FR_DEV_LABEL, MTNT_EN_FR_DEV = "mtnt_valid", os.path.join(PROJECT_PATH, "./data/MTNT/valid/valid.en-fr.conll")
MTNT_EN_FR_TEST_LABEL, MTNT_EN_FR_TEST = "mtnt_test", os.path.join(PROJECT_PATH, "./data/MTNT/test/test.en-fr.conll")
MTNT_EN_FR_TEST_DEMO_LABEL, MTNT_EN_FR_TEST_DEMO = "mtnt_test.demo", os.path.join(PROJECT_PATH, "./data/MTNT/test/test.en-fr.demo.conll")

## MTNT CONLL tokenized

MTNT_EN_TOK_TRAIN_CONLL_LABEL, MTNT_EN_TOK_TRAIN_CONLL = "mtnt_tok_train_conll", \
                                                         os.path.join(PROJECT_PATH, "./data/MTNT/monolingual/train.tok.en.conll")
MTNT_EN_TOK_DEV_CONLL_LABEL, MTNT_EN_TOK_DEV_CONLL = "mtnt_tok_dev_conll", \
                                                     os.path.join(PROJECT_PATH, "./data/MTNT/monolingual/dev.tok.en.conll")
MTNT_EN_TOK_DEV_DEMO_CONLL_LABEL, MTNT_EN_TOK_DEV_DEMO_CONLL = "mtnt_tok_dev_demo_conll", \
                                                               os.path.join(PROJECT_PATH, "./data/MTNT/monolingual/dev.tok.en.demo.conll")

#PERMUTATION
PERMUTATION_TRAIN_LABEL, PERMUTATION_TRAIN = "permutation-train", \
                                             os.path.join(PROJECT_PATH, "./data/permutation-train.conll")
PERMUTATION_TEST_LABEL, PERMUTATION_TEST= "permutation-test", \
                                          os.path.join(PROJECT_PATH, "./data/permutation-test.conll")
PERMUTATION_TRAIN_DIC = {}
PERMUTATION_TRAIN_LABEL_DIC = {}
for n_sent in [100, 1000, 10000, 50000, 100000, 200000]:
    dir_train = "{}-{}{}".format(PERMUTATION_TRAIN[:-6], n_sent, PERMUTATION_TRAIN[-6:])
    PERMUTATION_TRAIN_DIC[n_sent] = dir_train
    PERMUTATION_TRAIN_LABEL_DIC[n_sent] = "permutation-{}-train".format(n_sent)

# augmented data
AUGMENTATION_DIC = {}
AUGMENTATION_DIC_LABEL = {}
AUGMENTED_LEX_DIC = {}
AUGMENTED_LEX_DIC_LABEL = {}
GENERATED_DIC = {}
GENERATED_DIC_LABEL = {}

dic_dir_ls = [GENERATED_DIC, AUGMENTATION_DIC, AUGMENTED_LEX_DIC]
dic_label_ls = [GENERATED_DIC_LABEL, AUGMENTATION_DIC_LABEL, AUGMENTED_LEX_DIC_LABEL]

for n_sent in [50, 80, 100, 120,150, 250, 350, 500, 1000]:
    for dic_dir, dic_label, augmented in zip(dic_dir_ls, dic_label_ls, ["", "liu_owoputi_", "lexnorm15_train_data_"]):
        dir_train = os.path.join(PROJECT_PATH, "data", "back_normalized",
                                 augmented+"9326829-B-fbbe9-en_lines_ewt_train-noisy_generated_{}.conll").format(n_sent,".conll")
        dic_dir[n_sent] = dir_train
        dic_label[n_sent] = augmented+"9326829_B_fbbe9_en_lines_ewt_train_noisy_generated_{}".format(n_sent)


# EMOJIs
EMOJI_LS_LABEL, EMOJIS_LS = "emojis", os.path.join(PROJECT_PATH, "data/emojis_ls.txt")

# EN
EN_LINES_TRAIN_LABEL, EN_LINES_TRAIN = "en_lines_train", os.path.join(PROJECT_PATH, "../parsing/normpar/data/en_lines-ud-train.conllu")
EN_LINES_EWT_TRAIN_LABEL, EN_LINES_EWT_TRAIN = "en_lines_ewt_train", os.path.join(PROJECT_PATH, "../parsing/normpar/data/en_lines+ewt-ud-train.conllu")

EN_LINE_EWT_GUM_PARTUT_TRAIN_LABEL, EN_LINE_EWT_GUM_PARTUT_TRAIN = "en_lines-en_ewt-en_gum-en_partut-ud-train", os.path.join(PROJECT_PATH, "./data/en_lines-en_ewt-en_gum-en_partut-ud-train.conllu")


EN_LINES_DEV_LABEL, EN_LINES_DEV = "en_lines_dev", os.path.join(PROJECT_PATH, "../parsing/normpar/data/en_lines-ud-dev.conllu")

# SENT conll like
DEMO_SENT_LABEL, DEMO_SENT = "lexnorm-Demo_sent", os.path.join(PROJECT_PATH, "../parsing/normpar/data/char_test.demo")
TEST_SENT_LABEL, TEST_SENT = "lexnorm_sent", os.path.join(PROJECT_PATH, "../parsing/normpar/data/lexnorm-sent.conll")
DEV_SENT_LABEL, DEV_SENT = "owoputi_sent", os.path.join(PROJECT_PATH, "../parsing/normpar/data/owoputi-sent.conll")
LIU_TRAIN_SENT_LABEL, LIU_TRAIN_SENT = "liu_train_sent", os.path.join(PROJECT_PATH,
                                                                      "./data/LiLiu/2577_tweets-li-sent-train_2009.conll")
LIU_DEV_SENT_LABEL, LIU_DEV_SENT = "liu_dev_sent", os.path.join(PROJECT_PATH,
                                                                "./data/LiLiu/2577_tweets-li-sent-dev_500.conll")
# ERIC data
ERIC_ORIGINAL_LABEL, ERIC_ORIGINAL = "eric_frmg_original", \
                                     os.path.join(PROJECT_PATH,
                                                  "./data/eric_normalization/frmg_normalize4/collect2.nw100.conllu")
ERIC_ORIGINAL_DEMO_LABEL, ERIC_ORIGINAL_DEMO = "eric_frmg_original-demo", \
                                     os.path.join(PROJECT_PATH,
                                                  "./data/eric_normalization/frmg_normalize4/collect2.nw100-demo1000.conllu")

# WNUT-2015 ressources
EMNLP12_DIC_LABEL, EMNLP12_DIC = "emnlp-dic-wnut", os.path.join(PROJECT_PATH, "data/wnut-2015-ressources/emnlp2012-lexnorm/emnlp_dict.txt")


REPO_DATASET = {TRAINING: TRAINING_LABEL, DEV: DEV_LABEL, DEMO: DEMO_LABEL, DEMO2: DEMO2_LABEL,
                TEST: TEST_LABEL, LIU: LIU_LABEL,
                LEX_TRAIN_SPACE_DEMO: LEX_TRAIN_SPACE_DEMO_LABEL,
                LIU_TRAIN_OWOPUTI_LEX_TRAIN: LIU_TRAIN_OWOPUTI_LEX_TRAIN_LABEL,
                LIU_DEV_OWOPUTI: LIU_DEV_OWOPUTI_LABEL,
                LEX_TRAIN_SPLIT: LEX_TRAIN_SPLIT_LABEL,
                LEX_DEV_SPLIT:  LEX_DEV_SPLIT_LABEL,
                EN_LINE_EWT_GUM_PARTUT_TRAIN: EN_LINE_EWT_GUM_PARTUT_TRAIN_LABEL,
                LIU_OWOPUTI: LIU_OWOPUTI_LABEL,
                LEX_TRAIN: LEX_TRAIN_LABEL,
                LEX_TEST: LEX_TEST_LABEL,
                LEX_LIU_TRAIN: LEX_LIU_LABEL,
                LIU_DEV: LIU_DEV_LABEL, LIU_TRAIN: LIU_TRAIN_LABEL, LIU_TRAIN_OWOPUTI: LIU_TRAIN_OWOPUTI_LABEL,
                EWT_DEV: EWT_DEV_LABEL,
                CP_PASTE_TRAIN: CP_PASTE_TRAIN_LABEL, CP_PASTE_DEV: CP_PASTE_DEV_LABEL,
                CP_PASTE_TEST: CP_PASTE_TEST_LABEL,
                CP_PASTE_WR_TRAIN: CP_PASTE_WR_TRAIN_LABEL, CP_WR_PASTE_DEV: CP_PASTE_WR_DEV_LABEL,
                CP_WR_PASTE_TEST: CP_PASTE_WR_TEST_LABEL, CP_WR_PASTE_TEST_269: CP_PASTE_WR_TEST_269_LABEL,
                DEMO_SENT: DEMO_SENT_LABEL,
                TEST_SENT: TEST_SENT_LABEL, DEV_SENT: DEV_SENT_LABEL, LIU_TRAIN_SENT: LIU_TRAIN_SENT_LABEL,
                LIU_DEV_SENT: LIU_DEV_SENT_LABEL,
                EWT_TEST:EWT_TEST_LABEL,
                EN_LINES_TRAIN: EN_LINES_TRAIN_LABEL, EN_LINES_DEV: EN_LINES_DEV_LABEL,
                EN_LINES_EWT_TRAIN: EN_LINES_EWT_TRAIN_LABEL,
                MTNT_TOK_TRAIN: MTNT_TOK_TRAIN_LABEL, MTNT_TOK_DEV: MTNT_TOK_DEV_LABEL,
                MTNT_EN_FR_TRAIN: MTNT_EN_FR_TRAIN_LABEL,
                MTNT_EN_FR_DEV: MTNT_EN_FR_DEV_LABEL, MTNT_EN_FR_TEST: MTNT_EN_FR_TEST_LABEL,
                DIR_TWEET_W2V: TWEET_W2V_LABEL, FASTEXT_WIKI_NEWS_W2V_LABEL: DIR_FASTEXT_WIKI_NEWS_W2V,
                MTNT_EN_FR_TEST_DEMO: MTNT_EN_FR_TEST_DEMO_LABEL,
                EWT_PRED_TOKEN_UDPIPE: EWT_PRED_TOKEN_UDPIPE_LABEL,
                MTNT_EN_TOK_TRAIN_CONLL: MTNT_EN_TOK_TRAIN_CONLL_LABEL,
                MTNT_EN_TOK_DEV_CONLL: MTNT_EN_TOK_DEV_CONLL_LABEL,
                MTNT_EN_TOK_DEV_DEMO_CONLL: MTNT_EN_TOK_DEV_DEMO_CONLL_LABEL,
                EMOJIS_LS: EMOJI_LS_LABEL,
                PERMUTATION_TRAIN: PERMUTATION_TRAIN_LABEL, PERMUTATION_TEST: PERMUTATION_TEST_LABEL,
                ERIC_ORIGINAL: ERIC_ORIGINAL_LABEL,
                EMNLP12_DIC: EMNLP12_DIC_LABEL
                }


for n_sent in [100, 1000, 10000, 50000, 100000, 200000]:
    REPO_DATASET[PERMUTATION_TRAIN_DIC[n_sent]] = PERMUTATION_TRAIN_LABEL_DIC[n_sent]
for n_sent in [50, 80, 100, 120,150,250,350, 500, 1000]:
    REPO_DATASET[AUGMENTATION_DIC[n_sent]] = AUGMENTATION_DIC_LABEL[n_sent]
    REPO_DATASET[AUGMENTED_LEX_DIC[n_sent]] = AUGMENTED_LEX_DIC_LABEL[n_sent]
    REPO_DATASET[GENERATED_DIC[n_sent]] = GENERATED_DIC_LABEL[n_sent]


REPO_LABEL2SET = {v:k for k,v in REPO_DATASET.items()}

REPO_W2V = {
            DIR_TWEET_W2V: {"label": TWEET_W2V_LABEL, "dim": 400},
            DIR_FASTEXT_WIKI_NEWS_W2V: {"label": FASTEXT_WIKI_NEWS_W2V_LABEL, "dim": 300},
            None: {"label": "random_init", "dim": -1}
            }


# for some task we need normalize = True for getting the label
# NB : predicted_classes does not necessarily mean that the task is to predict those classes but that
# it can be deduced in a straitforward way from he prediciton !!
TASKS_PARAMETER = {"normalize": {"normalization": True, "default_metric": "exact_match",
                                 "predicted_classes": ["NORMED", "NEED_NORM"]},
                   "norm_not_norm": {"normalization": True},
                   "edit_prediction": {"normalization": True},
                   "pos": {"normalization": False, "default_metric": "accuracy-pos"},
                   "all": {"normalization": True}}


# output dir for writing
WRITING_DIR = os.path.join(PROJECT_PATH, "predictions")

WARMUP_N_EPOCHS = 1

EPSILON = 1e-3

# FOR NOW HERE , should be shared with experimental pipe prokect (should come from it actualy)
REPORT_FLAG_DIR_STR = "NEW REPORT : overall report saved "
REPORT_FLAG_VARIABLES_ENRICH_STR = "GRID_INFO enrch vars= "
REPORT_FLAG_VARIABLES_EXPAND_STR = "GRID_INFO metric    = "
REPORT_FLAG_VARIABLES_FIXED_STR = "GRID_INFO fixed vals="
REPORT_FLAG_VARIABLES_ANALYSED_STR = "GRID_INFO analy vars= "
