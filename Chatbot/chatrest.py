# -*- coding: utf-8 -*-
"""
Created on 14 Nov 2017

@author: Rishabh.gupta
"""

import web, sys, os, json
import config as cfg
import logging, traceback

if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import conversation_engine

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout,level=logging.INFO,format=FORMAT)
# logging.basicConfig(filename=cfg.LOGGER_FILE_NAME,level=logging.INFO,format=FORMAT)
# stdoutLogger = logging.StreamHandler()
# logging.getLogger().addHandler(stdoutLogger)
logger = logging.getLogger(__name__)


urls = (
'/bot','Bot'
)
app = web.application(urls, globals())


class Bot:
    def GET(self):
        try:
            logger.info("####################################")
            web.header('Content-Type', 'application/json')
            user_data = web.input()
            query = str(user_data.query)
            user_name = str(user_data.user_name)
            company_name = str(user_data.company_name)
            request_type = str(user_data.request_type)
            logger.info("Input params:: Query- %s :: Company- %s",query, company_name)
            logger.info("request_type- %s :: User- %s", request_type, user_name )
            print query
            resp = conversation_engine.wrapper(query, user_name, company_name)
            result = json.loads(resp)
            logger.info("Response returned as follows :")
            logger.info("Answer: %s", result['Answer'])
            logger.info("Confidence: %s",result['Confidence'])
            logger.info("Status_code: %s", result['Status_code'])
            return resp
        except Exception as e:
            logger.error("Error occurred: %s", e)
            logger.error(traceback.format_exc())
            answer = cfg.ERROR_MSG
            confidence = 0
            status = 400
            return conversation_engine.prepare_answer(answer, confidence, status)

if __name__ == "__main__":


    app.run()


