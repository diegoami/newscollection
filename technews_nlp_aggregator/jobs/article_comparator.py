import logging


from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence import ArticleDatasetRepo, ArticlesSimilarRepo
import yaml
from datetime import date


import traceback


class ArticleComparatorJob:

    def __init__(self, db_connection, facade, thresholds):
        self.similarArticlesRepo = ArticlesSimilarRepo(db_connection)

        self.facade = facade
        self.article_loader = self.facade.article_loader

        self.thresholds = thresholds
        self.inserted_in_session = set()

    def save_job_execution(self, start, end):
        self.similarArticlesRepo.persist_job(start, end, self.facade.name, self.thresholds  )

