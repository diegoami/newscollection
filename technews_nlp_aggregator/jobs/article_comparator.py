import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence import ArticleDatasetRepo, SimilarArticlesRepo
import yaml
from datetime import date


import traceback


class ArticleComparatorJob:

    def __init__(self, db_connection, facade, thresholds):
        self.similarArticlesRepo = SimilarArticlesRepo(db_connection)

        self.facade = facade
        self.article_loader = self.facade.article_loader

        self.thresholds = thresholds
        self.inserted_in_session = set()

    def save_job_execution(self, start, end):
        self.similarArticlesRepo.persist_job(start, end, self.facade.name, self.thresholds  )

    def find_articles(self, start, end):
        articles_and_sims= self.facade.compare_articles_from_dates(start, end, self.thresholds )
        articlesDF = self.article_loader.articlesDF
        con = self.similarArticlesRepo.get_connection()

        for id, sims in articles_and_sims.items():
            try:
                con.begin()

                for other_id, score in sims:
                    article, otherarticle = articlesDF.iloc[id], articlesDF.iloc[other_id]
                    article_id, article_other_id = article['article_id'] , otherarticle ['article_id']
                    if ((article_id, article_other_id ) not in self.inserted_in_session):
                        self.similarArticlesRepo.persist_association(con, article_id, article_other_id, self.facade.name, score )
                        self.inserted_in_session.add((article_id, article_other_id))
                con.commit()
            except:
                traceback.print_exc()
                con.rollback()


