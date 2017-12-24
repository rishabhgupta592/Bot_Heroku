# -*- coding: utf-8 -*-
"""
Created on 14 Nov 2017

@author: Rishabh.gupta
"""

import os, sys, json
import pandas as pd
import numpy as np
import cPickle as pickle
from sklearn.feature_extraction.text import TfidfVectorizer
if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config as cfg
from data_preparation.vocab_gen import build_vocab
from data_preparation.spell_model_building import build_spell_model
from data_preparation.Data_prep import data_preparation as dp

def train(company_list):
    # Build vocabulary
    for company_name in company_list:
        print "** Model Building start for company :: "+company_name +" **"
        build_vocab(company_name)
        print "Vocab building done."
        # Train spell check model
        build_spell_model(company_name)
        print "Spell model building done"

        print "TF-IDF building started ..."
        data_file_path = cfg.INPUT_PATH + "/" + company_name +".csv"
        data = pd.read_csv(data_file_path)
        content = data.Que
        prepared_content = [' '.join(dp.data_prep(article, company_name)) for article in content]
        tfidf_vectorizer = TfidfVectorizer(max_features=20000, use_idf=True,
                                           max_df=1.0, min_df=0.001,
                                           ngram_range=(1, 3), sublinear_tf=True)
        tfidf_matrix = tfidf_vectorizer.fit_transform(prepared_content)
        vocabulary = tfidf_vectorizer.vocabulary_
        idf = tfidf_vectorizer.idf_
        mat = tfidf_vectorizer._tfidf._idf_diag
        # Creating the folder if not exist else place in the already existing folder
        _dir = cfg.MODEL_PATH + "/" + company_name + "/"
        if not os.path.exists(_dir):
            os.makedirs(_dir)

        np.save((os.path.join(_dir, 'idf')), idf)
        with open((os.path.join(_dir, 'tfidf_matrix.dat')), 'wb') as outfile:
            pickle.dump(tfidf_matrix, outfile, pickle.HIGHEST_PROTOCOL)
        json.dump(vocabulary, open((os.path.join(_dir, 'vocabulary.json')), mode='wb'))
        with open((os.path.join(_dir, 'mat.dat')), 'wb') as oo:
            pickle.dump(mat, oo, pickle.HIGHEST_PROTOCOL)
        terms = tfidf_vectorizer.get_feature_names()
        df = pd.DataFrame(terms, columns=["terms"])
        print "TF-IDF building done."

if __name__ == "__main__":
    # Data csv name should be same
    company_list = ["bank"]
    train(company_list)
