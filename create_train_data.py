

import yaml
import pandas as pd
import sys
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.application import Application
from technews_nlp_aggregator.prediction import FeatureFiller
import argparse
from technews_nlp_aggregator.common import load_config
def direct_confront(feature_filler, similarArticlesRepo):


    user_paired = similarArticlesRepo.retrieve_user_paired()
    logging.info("Retrieved {} userpaired".format(len(user_paired)))

    retrieves_scores(user_paired, feature_filler, similarArticlesRepo)

def retrieves_scores(user_paired, feature_filler, similarArticlesRepo):
    score_list = []
    added, updated, untouched = 0, 0, 0
    con = similarArticlesRepo.get_connection()
    for index, row in enumerate(user_paired):
        article_id1, article_id2, similarity = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2'],  row['SSU_SIMILARITY']
        found_score = similarArticlesRepo.score_exists({"SCO_AIN_ID_1": article_id1, "SCO_AIN_ID_2": article_id2,
                                                 "SCO_VERSION": feature_filler.version}, con)
        if not found_score:
            logging.debug("Adding score for {} {}".format(article_id1, article_id2))
            added += 1
            score = feature_filler.fill_score_map( article_id1, article_id2)
            similarArticlesRepo.insert_score(score, con)
            logging.info("Score : {}".format(score))
        elif found_score["SCO_W_DAYS"] is None:
            updated += 1
            logging.debug("Updating score for {} {}".format(article_id1, article_id2))

            found_score["SCO_W_DAYS"] = feature_filler.calc_work_days(article_id1, article_id2)
            similarArticlesRepo.update_score(found_score, con)
        else:
            untouched += 1
            logging.debug("Found score for {} {}".format(article_id1, article_id2))

        if (index % 100 == 1):
            logging.info("Processed {} rows".format(index))

    logging.info("Added: {}, Updated: {}, Untouched: {}".format(added, updated, untouched))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    args = parser.parse_args()
    config_file = sys.argv[1] if (len(sys.argv) > 1) else 'config.yml'
    config = yaml.safe_load(open(config_file))

    version = config["version"]
    application = Application(config, True)
    feature_filler = FeatureFiller(articleLoader=application.articleLoader, summaryFacade=application.summaryFacade, tfidfFacade=application.tfidfFacade, doc2VecFacade=application.doc2VecFacade, classifierAggregator=application.classifierAggregator,
                                   tf2wv_mapper=application.tf2wv_mapper, version=version)
    similarArticlesRepo = application.similarArticlesRepo
    application.gramFacade.load_phrases()
    direct_confront( feature_filler, similarArticlesRepo)




