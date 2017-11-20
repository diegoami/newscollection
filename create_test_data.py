

import yaml
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.application import Application
from technews_nlp_aggregator.prediction import FeatureFiller
import argparse


def create_test_data( test_file, starting_date, feature_filler, similarArticlesRepo):
    test_data = similarArticlesRepo.retrieve_similar_since( starting_date)
    logging.info("Retrieved {} ".format(len(test_data)))
    score_list_test  = retrieves_test( test_data, feature_filler, similarArticlesRepo )
    df = pd.DataFrame(score_list_test )
    print(df.head())
    df.to_csv( test_file)


def retrieves_test(test_data, feature_filler, similarArticlesRepo ):
    score_list = []
    con = similarArticlesRepo.get_connection()
    for index, row in enumerate(test_data):

        article_id1, article_id2= row['SST_AIN_ID_1'], row['SST_AIN_ID_2']
        if not similarArticlesRepo.score_exists({"SCO_AIN_ID_1" : article_id1, "SCO_AIN_ID_2" : article_id2, "SCO_VERSION" : FeatureFiller.CURRENT_VERSION  }, con):
            score = feature_filler.fill_score_map( article_id1, article_id2)
            similarArticlesRepo.insert_score(score, con)
            logging.info("Score : {}".format(score))
            score_list.append(score)
            if (index % 100 == 0):
                logging.info("Processed {} rows".format(index))
    return score_list




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sincewhen', help='since when')
    args = parser.parse_args()

    config = yaml.safe_load(open('config.yml'))

    train_fail_loc = config["train_data_file"]
    test_fail_loc = config["test_data_file"]

    application = Application(config, True)
    feature_filler = FeatureFiller(articleLoader=application.articleLoader, summaryFacade=application.summaryFacade, tfidfFacade=application.tfidfFacade, doc2VecFacade=application.doc2VecFacade, classifierAggregator=application.classifierAggregator)
    similarArticlesRepo = application.similarArticlesRepo
    application.gramFacade.load_phrases()


    create_test_data(test_fail_loc, args.sincewhen, feature_filler, similarArticlesRepo)
