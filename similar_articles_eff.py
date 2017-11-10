import sys

import yaml
from technews_nlp_aggregator.jobs import ArticleComparatorJob
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.common.util import daterange
from datetime import datetime, timedelta

from technews_nlp_aggregator import Application

def eff_similar_articles(application):
    _ = application
    articlesToProcessDF =  _.articleDatasetRepo.load_articles_for_process()
    for index, row in articlesToProcessDF.iterrows():
        article_id = row['AIN_ID']
        article_date = row['AIN_DTE']

        related_articles_tdf = _.tfidfFacade.get_related_articles_for_id(_.articleLoader.articlesDF, 2, index, article_date)
        related_articles_doc2vec = _.doc2VecFacade.get_related_articles_for_id(_.articleLoader.articlesDF, 2, index, article_date)

        process_for_insertion(related_articles_tdf)
        process_for_insertion(related_articles_doc2vec)


if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))
    application = Application(config, True)
    eff_similar_articles(application)
