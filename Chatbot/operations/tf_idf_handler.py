# -*- coding: utf-8 -*-
"""
Created on 14 Nov 2017

@author: Rishabh.gupta
"""
import os, json, sys
import config as cfg
import cPickle as pickle
import numpy as np

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from  operations import cosine_similarity


def fetch_score(prepared_query, company_name):
    # Search the Questions model
    # Loading all the saved tfidf models
    model_path = cfg.MODEL_PATH + "/"+ company_name
    with open((os.path.join(model_path, 'tfidf_matrix.dat')), 'rb') as infile:
        tfidf_mat = pickle.load(infile)

    with open((os.path.join(model_path, 'mat.dat')), 'rb') as ii:
        mat = pickle.load(ii)
    vocab = json.load(open((os.path.join(model_path, 'vocabulary.json')), mode='rb'))
    idf = np.load((os.path.join(model_path, 'idf.npy')))
    score = cosine_similarity.get_cosine_similarity(prepared_query, tfidf_mat, vocab, mat, idf)
    if (score.isnull().values.any() == True):
        score = score.fillna(value=0)
    return score.head(1)

if __name__ == "__main__":

    fetch_score("abc")