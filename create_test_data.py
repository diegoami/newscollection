

import yaml
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.application import Application
from technews_nlp_aggregator.prediction import FeatureFiller
import argparse
from datetime import timedelta

def create_test_data( test_file, starting_date, feature_filler, similarArticlesRepo, until_date=None):
    test_data = similarArticlesRepo.retrieve_similar_since( starting_date, until_date)
    logging.info("Retrieved {} ".format(len(test_data)))
    retrieves_test( test_data, feature_filler, similarArticlesRepo)


def retrieves_test(test_data, feature_filler, similarArticlesRepo ):

    con = similarArticlesRepo.get_connection()
    for index, row in enumerate(test_data):

        article_id1, article_id2= row['SST_AIN_ID_1'], row['SST_AIN_ID_2']

        if not similarArticlesRepo.score_exists({
                                                 "SCO_AIN_ID_1" : article_id1,
                                                 "SCO_AIN_ID_2" : article_id2,
                                                 "SCO_VERSION" : feature_filler.version  }, con):
            logging.info("Processing {}, {}".format(article_id1, article_id2))
            try:
                score = feature_filler.fill_score_map( article_id1, article_id2)
                similarArticlesRepo.insert_score(score, con)
                logging.info("Score : {}".format(score))
            except:
                logging.warn("Error trying to process: {}, {}".format(article_id1, article_id2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sincewhen', help='since when')
    parser.add_argument('--untilwhen', help='until when')
    args = parser.parse_args()

    config = yaml.safe_load(open('config.yml'))

    train_fail_loc = config["train_data_file"]
    test_fail_loc = config["test_data_file"]
    version = config["version"]

    application = Application(config, True)
    if args.sincewhen:
        sincewhen = args.sincewhen
    else:
        latest_article_date = application.app.articleDatasetRepo.get_latest_article_date()
        sincewhen_date = latest_article_date - timedelta(7)
        sincewhen = str(sincewhen_date.year) + '-' + str(sincewhen_date.month) + '-' + str(sincewhen_date.day)

    if args.untilwhen:
        untilwhen = args.untilwhen
    else:
        untilwhen = None

    feature_filler = FeatureFiller(articleLoader=application.articleLoader, summaryFacade=application.summaryFacade, tfidfFacade=application.tfidfFacade, doc2VecFacade=application.doc2VecFacade, classifierAggregator=application.classifierAggregator, version=version)
    similarArticlesRepo = application.similarArticlesRepo
    application.gramFacade.load_phrases()
    create_test_data(test_file=test_fail_loc, starting_date=sincewhen, feature_filler=feature_filler, similarArticlesRepo=similarArticlesRepo, until_date=untilwhen)
