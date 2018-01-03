# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import math
from scipy.spatial.distance import cosine
import os, sys

# if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path:
    # sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_preparation.Data_prep import data_preparation as dp


def get_cosine_similarity(query,tfidf_mat,vocab,mat,idf):
    # print "In cosine sim"
    #print query
    class MyVectorizer(TfidfVectorizer):
        # plug our pre-computed IDFs
        TfidfVectorizer.idf_ = idf
    
    vectorizer  = MyVectorizer(max_features=20000, use_idf=True,
                                           max_df=1.0, min_df=0.001,
                                           ngram_range=(1,3), sublinear_tf=True )
    #plugging the diagonal elements
    vectorizer._tfidf._idf_diag = mat
    #pluging the vocabulary
    vectorizer.vocabulary_ = vocab
    #Fitting and trasforming the user query and getting the tfidf values for all the words
    response = vectorizer.transform([query])
    
    #Cosine similarity calculation 
    a = tfidf_mat.shape[0]
    #print "a ", a
    query_vec = response.toarray()
    #print "Query vec ", query_vec.tolist()
    cosine_sim_vals = [1-cosine(query_vec, tfidf_mat[i].toarray()) for i in range(a)]
    #cosine_sim_vals = [for i in cosine_sim_vals]
    
    cosine_sim_vals = pd.DataFrame(cosine_sim_vals)
    #print "vocab : ", vocab
    #print cosine_sim_vals
    cosine_sim = cosine_sim_vals.sort_values(0, ascending=False)
    # print "\nTop 5 similarities : \n", cosine_sim.head()
    return cosine_sim
