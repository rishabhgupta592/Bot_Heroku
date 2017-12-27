# -*- coding: utf-8 -*-
"""
Created on 14 Nov 2017

@author: Rishabh.gupta
"""

import os, sys, json, re
import logging
import pandas as pd
import random
import string
import random
logger = logging.getLogger(__name__)

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_preparation.Data_prep import data_preparation as dp
from operations import tf_idf_handler
import config as cfg


def prepare_answer(answer, confidence, status_code, response_type):
    answer = [unicode(ans, errors='ignore') for ans in answer]
    response_type = unicode(response_type, errors='ignore')
    json_data = {"Answer": answer,
                 "Confidence": round(confidence * 100, 2),
                 "typeOfResponse": response_type,
                 "Suggestions": [],
                 'Status_code': status_code,
                 "Intent": "bank"
                 }
    return json.dumps(json_data)


def fetch_answer(data, max_index):
    answer_frame = data.iloc[:, 3:]
    answer = answer_frame.loc[max_index].dropna().values.tolist()
    response_type = data["Type"].loc[max_index]
    response_type = response_type.lower()
    if response_type == "random":
        response_type = "text"
        answer = [random.choice(answer)]
    return answer, response_type


def wrapper(query, user_name, company_name):
    """ Main method which will work as handler"""

    # Data prepration of Query
    logger.info("Incoming query: %s", query)
    if query == "getWelcomeMessage":
        wlc_msg = random.choice(cfg.WELCOME_MSG)
        wlc_msg = string.replace(wlc_msg, '[name]', user_name)
        return prepare_answer(wlc_msg, 1, 200)
    query = query.lower().strip()
    query = re.sub(r"[^A-Za-z0-9]", " ", query)
    ignore_stop_word_query = ["who are you", "how are you"]
    if query not in ignore_stop_word_query:
        prepared_query = ' '.join(dp.data_prep(query, company_name, check_spellings=False))
    else:
        if query == ignore_stop_word_query[0]:
            return prepare_answer(["I am Chatbot, your virtual assistant."], 100, 200, "text")
        elif query == ignore_stop_word_query[1]:
            return prepare_answer(["Thanks, am doing good."], 100, 200, "text")

    logger.info("Prepared query: %s", prepared_query)
    answer = tf_idf_handler.fetch_score(prepared_query, company_name)

    max_index = answer.index.tolist()[0]
    max_score = answer.values.tolist()[0][0]
    logger.info(max_score)
    if max_score > cfg.THRESHOLD:
        data_file = cfg.INPUT_PATH + company_name + ".csv"
        data = pd.read_csv(data_file)
        confidence = max_score
        # answer = data.Answer.get_value(max_index)
        status = cfg.SUCCESS_STATUS_CODE
        answer, response_type = fetch_answer(data, max_index)
    else:
        answer = [cfg.ANSWER_NOT_FOUND_MSG]
        status = cfg.ANSWER_NOT_FOUND_CODE
        confidence = 0
        response_type = "text"
    return prepare_answer(answer, confidence, status, response_type)