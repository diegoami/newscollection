import traceback

import dataset
from technews_nlp_aggregator.common.util import extract_host, extract_normpath, extract_source_without_www

class ArticlesSpiderRepo:

    def get_connection(self):
        return self.dataset_connection

    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.dataset_connection = dataset.connect(self.db_connection, engine_kwargs={
            'connect_args': {'charset': 'utf8'}
        })
        self.engine = self.dataset_connection.engine

    def retrieve_urls_queued(self):
        sql_user_similar = "SELECT UTA_SPIDER, UTA_URL FROM URLS_TO_ADD WHERE UTA_PROCESSED IS NULL"
        similar_stories = []
        con = self.get_connection()
        query_result= con.query(sql_user_similar )
        result = [(row["UTA_SPIDER"], row["UTA_URL"].strip()) for row in query_result]
        return result

    def add_url_list(self, url_list):
        sql_add_user = "INSERT INTO URLS_TO_ADD (UTA_SPIDER, UTA_URL) VALUES (:uta_spider, :uta_url) "
        con = self.get_connection()
        messages = []
        for url in url_list:
            url = extract_normpath(url)
            host = extract_source_without_www(url).lower().capitalize()
            try:
                con.begin()
                con.query(sql_add_user , {"uta_spider": host, "uta_url": url.strip()})
                messages.append("Added {} : {}".format(host, url))
                con.commit()
            except:
                con.rollback()
                traceback.print_stack()
        return messages


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