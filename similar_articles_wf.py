import sys

import yaml
from technews_nlp_aggregator.jobs import ArticleComparatorJob
import logging

from technews_nlp_aggregator.common.util import daterange
from datetime import datetime, timedelta

from technews_nlp_aggregator import Application

def persist_similar_articles(application):

    def find_with_model(model, thresholds, begin, finish, days_diff):
        articleComparatorJob = ArticleComparatorJob(db_url, model, thresholds)

        for start, end in daterange(begin, finish, days_diff):
            logging.info("Now processing articles between {} and  {}".format (start, end))
            articleComparatorJob.find_articles(start, end)

    _ = application
    max_art_date = application.articleDatasetRepo.get_latest_article_date()
    max_sim_date = application.similarArticlesRepo.get_last_similar_story()
    start = max_sim_date - timedelta(days=3)
    end   = max_art_date + timedelta(days=2)

    db_url = _.db_url

    find_with_model(model = _.tfidfFacade, thresholds = (0.64, 0.995),
                    begin = start, finish = end, days_diff=2)

    find_with_model(model = _.doc2VecFacade, thresholds = (0.27, 0.99),
                    begin = start,  finish = end, days_diff=2)

if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))
    application = Application(config, True)
    persist_similar_articles(application)
