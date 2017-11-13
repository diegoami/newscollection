import logging
import traceback
from datetime import datetime
import pandas as pd
import dataset
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer


import re
from technews_nlp_aggregator.common.util import extract_source


class ArticlesSpiderRepo:

    def get_connection(self):
        con = dataset.connect(self.db_connection, engine_kwargs={
            'connect_args': {'charset': 'utf8'}
        })
        return con

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def retrieve_urls_queued(self):
        sql_user_similar = "SELECT UTA_SPIDER, UTA_URL FROM URLS_TO_ADD WHERE UTA_PROCESSED IS NULL"
        similar_stories = []
        con = self.get_connection()
        query_result= con.query(sql_user_similar )
        result = [row for row in query_result]
        return result

    def update_to_crawled(self, con=None):
        sql_update = "UPDATE URLS_TO_ADD SET UTA_PROCESSED = SYSDATE()"
        con = self.get_connection() if not con else con
        try:
            con.begin()
            article_query = con.query(sql_update)
            con.commit()
        except:
            con.rollback()
            traceback.print_stack()