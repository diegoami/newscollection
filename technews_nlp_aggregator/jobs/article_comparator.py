import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence import ArticleDatasetRepo, SimilarArticlesRepo
import yaml
from datetime import date





class ArticleComparatorJob:

    def __init__(self, db_connection, facade, thresholds):
        self.similarArticlesRepo = SimilarArticlesRepo(db_connection)

        self.facade = facade
        self.article_loader = self.facade.article_loader

        self.thresholds = thresholds

    def save_job_execution(self, start, end):
        self.similarArticlesRepo.persist_job(start, end, self.facade.name, self.thresholds  )

    def find_articles(self, start, end):
        articles_Found = self.facade.compare_articles_from_dates(start, end, self.thresholds )
        articlesDF = self.article_loader.articlesDF
        for art_cp, score in articles_Found.items():
            id, other_id = art_cp
            article, otherarticle = articlesDF.loc[id], articlesDF.loc[other_id]
            article_id, article_other_id = article['article_id'] , otherarticle ['article_id']
            self.similarArticlesRepo.persist_association(article_id, article_other_id, self.facade.name, score )
        self.save_job_execution(start, end)


