# -*- coding: utf-8 -*-
"""
Created on 14 Nov 2017

@author: Rishabh.gupta
"""


# ROOT = "D:/MyDoc/Project/airobotica/Source"
ROOT = "/app/Chatbot"
LOGGER_FILE_NAME = "Bot.log"

INPUT_PATH = ROOT + "/Data/"

MODEL_PATH = ROOT + "/Model/"

THRESHOLD = 0.4

ERROR_STATUS_CODE = 400

ERROR_MSG = "Oops! Sorry, I am not able to help you right now."

ANSWER_NOT_FOUND_CODE = 201

ANSWER_NOT_FOUND_MSG = "Sorry, not able to get answer for your query in current version."

SUCCESS_STATUS_CODE = 200

WELCOME_MSG = ["Hey [name] how is your week going?","Have a great week [name]!",
               "Hola [name] how are you doing?",
               "Is there anything I can help you with?",
               "How are you feeling today?"]