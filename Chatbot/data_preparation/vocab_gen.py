# -*- coding: utf-8 -*-
"""
Created on 14 Nov 2017

@author: Rishabh.gupta
"""

import os, sys, re
import pandas as pd

if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config as cfg
from data_preparation.Data_prep import data_preparation as dp


def build_vocab(company_name):
    file_path = cfg.INPUT_PATH + "/"+company_name+".csv"
    csv_reader = pd.read_csv(file_path)
    ####create vobab
    data = csv_reader.Que.values.tolist()
    answers = csv_reader.Answer.drop_duplicates().values.tolist()

    data = [dp.clean_str(dat) for dat in
            data]  # [unicodedata.normalize('NFKD', unicode(dat.lower())).encode('ascii','ignore') for dat in data]
    answers = [dp.clean_str(dat) for dat in
               answers]  # [unicodedata.normalize('NFKD', unicode(dat.lower(), 'ascii')).encode('ascii','ignore') for dat in answers]

    data.extend(answers)
    print "Dumping vocab file"

    str = ' '.join(data)  # convert to string
    bigfTxt = file(os.path.join(cfg.ROOT, 'data_preparation/Data_prep/Big.txt')).read()
    bigTxt = str + " " + bigfTxt
    directory = os.path.join(cfg.ROOT, 'data_preparation/vocab/'+company_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory+'/DataPrepCorpus.txt'), "wb") as text_file:
        text_file.write(bigTxt)
    return " Vocab Generation Done"


if __name__ == "__main__":
    status = build_vocab("Discover")
    print status
