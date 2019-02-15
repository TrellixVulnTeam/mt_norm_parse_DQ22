import numpy as np
from io_.info_print import printing


def load_emb(extern_emb_dir, verbose=0):
    loaded_dic = {}

    external_embedding_fp = open(extern_emb_dir, 'r', encoding='utf-8', errors='ignore')
    printing("W2V : Starting loading of {} ", var=[extern_emb_dir], verbose_level=1, verbose=verbose)
    for ind, line in enumerate(external_embedding_fp):
        line = line.strip().split()
        loaded_dic[line[0]] = [float(f) for f in line[1:]]
    dim = len([float(f) for f in line[1:]])
    external_embedding_fp.close()
    printing("MODEL : Word Embedding loaded form {} with  {} words of dim {} ", var=[extern_emb_dir, len(loaded_dic), dim], verbose=verbose, verbose_level=1)
    return loaded_dic