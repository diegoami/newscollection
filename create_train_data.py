

import yaml

import sys
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.application import Application
from technews_nlp_aggregator.model import FeatureFiller


def direct_confront(feature_filler, similarArticlesRepo, version):


    user_paired = similarArticlesRepo.retrieve_user_paired(version=version, for_assignment=True)
    logging.info("Retrieved {} userpaired".format(len(user_paired)))

    retrieves_scores(user_paired, feature_filler, similarArticlesRepo)

def retrieves_scores(user_paired, feature_filler, similarArticlesRepo):
    score_list = []
    added = 0
    con = similarArticlesRepo.get_connection()
    for index, row in enumerate(user_paired):
        article_id1, article_id2, similarity = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2'],  row['SSU_SIMILARITY']
        score = feature_filler.fill_score_map( article_id1, article_id2)
        similarArticlesRepo.insert_score(score, con)

        logging.info("Adding score for {} {} : {}".format(article_id1, article_id2, score))
        if (index % 100 == 1):
            logging.info("Processed {} rows".format(index))

    logging.info("Added: {} rows".format(added))

if __name__ == '__main__':
    config_file = sys.argv[1] if (len(sys.argv) > 1) else 'config.yml'
    config = yaml.safe_load(open(config_file))

    version = config["version"]
    application = Application(config, True)
    feature_filler = FeatureFiller(articleLoader=application.articleLoader, summaryFacade=application.summaryFacade, tfidfFacade=application.tfidfFacade, doc2VecFacade=application.doc2VecFacade, classifierAggregator=application.classifierAggregator,
                                   tf2wv_mapper=application.tf2wv_mapper, version=version)
    similarArticlesRepo = application.similarArticlesRepo
    application.gramFacade.load_phrases()
    direct_confront( feature_filler, similarArticlesRepo, version)




