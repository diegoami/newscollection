

import logging
import sys
import yaml

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.application import Application
from technews_nlp_aggregator.prediction import FeatureFiller
from technews_nlp_aggregator.common import load_config

import argparse
from datetime import timedelta
import sys

def create_test_data( starting_date, feature_filler, similarArticlesRepo, version, max_skipped=100):
    logging.info("Retrieving data starting from {}".format(starting_date))
    similarDF = similarArticlesRepo.retrieve_similar_since( starting_date, version)
    logging.info("Retrieved {} ".format(len(similarDF )))

    testDF = similarArticlesRepo.load_test_set(version=config["version"])
    logging.info("Test_df has {} rows".format(len(testDF)))
    mergedDF = similarDF[~similarDF.index.isin(testDF.index)]
    logging.info("merged_df has {} rows".format(len(mergedDF )))

    retrieves_test( mergedDF, feature_filler, similarArticlesRepo, max_skipped=max_skipped)


def retrieves_test( merged_DF, feature_filler, similarArticlesRepo, max_skipped=100 ):

    con = similarArticlesRepo.get_connection()
    skipped, added = 0, 0
    for index, row in merged_DF.iterrows():

        article_id1, article_id2 = index[0], index[1]

        score = feature_filler.fill_score_map( article_id1, article_id2)
        scores_found = similarArticlesRepo.insert_score(score, con)
        if not scores_found:
            skipped += 1
        else:
            added += 1

        if ((added+skipped) % 50 == 0):
            logging.info("Added {}, skipped {} rows".format(added, skipped))
        if skipped > max_skipped:
            logging.info("Skipped {} rows, leaving".format(skipped))
            break
    logging.info("Added {}, skipped {} rows".format(added, skipped))

if __name__ == '__main__':
    config_file = sys.argv[1] if (len(sys.argv) > 1) else 'config.yml'
    config = yaml.safe_load(open(config_file))

    version = config["version"]
    max_skipped = config.get("max_skipped", 100)
    application = Application(config, True)
    latest_article_date = application.articleDatasetRepo.get_latest_article_date()
    sincewhen_date = latest_article_date - timedelta(config["score_go_back"])
    sincewhen = str(sincewhen_date.year) + '-' + str(sincewhen_date.month) + '-' + str(sincewhen_date.day)

    feature_filler = FeatureFiller(articleLoader=application.articleLoader, summaryFacade=application.summaryFacade, tfidfFacade=application.tfidfFacade, doc2VecFacade=application.doc2VecFacade, classifierAggregator=application.classifierAggregator,
                                   tf2wv_mapper=application.tf2wv_mapper,version=version)
    similarArticlesRepo = application.similarArticlesRepo
    application.gramFacade.load_phrases()
    create_test_data(starting_date=sincewhen, feature_filler=feature_filler, similarArticlesRepo=similarArticlesRepo, version=version,
                     max_skipped=max_skipped)
