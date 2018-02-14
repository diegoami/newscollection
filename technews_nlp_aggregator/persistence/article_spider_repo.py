import traceback

import dataset


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