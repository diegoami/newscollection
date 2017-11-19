

import yaml
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.application import Application
from technews_nlp_aggregator.prediction import FeatureFiller
import argparse
def direct_confront(application, train_file, feature_filler):
    _ = application

    user_paired = _.similarArticlesRepo.retrieve_user_paired()

    scores = retrieves_scores(user_paired, feature_filler)
    df = pd.DataFrame(scores)
    print(df.head())
    df.to_csv(train_file)

def create_test_data(application, test_file, starting_date, feature_filler):

    _ = application

    test_data = _.similarArticlesRepo.retrieve_similar_since( starting_date)
    logging.info("Retrieved {} ".format(len(test_data)))
    test  = retrieves_test( test_data, feature_filler )

    df = pd.DataFrame(test )
    print(df.head())
    df.to_csv( test_file)


def retrieves_scores(user_paired, feature_filler):
    score_list = []
    for index, row in enumerate(user_paired):

        article_id1, article_id2, similarity = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2'],  row['SSU_SIMILARITY']
        score = feature_filler.fill_score_map( article_id1, article_id2)

        score["SCO_USER"] = similarity
        logging.info("Score : {}".format(score))
        score_list.append(score)
        if (index % 100 == 0):
            logging.info("Processed {} rows".format(index))
    return score_list


def retrieves_test(test_data, feature_filler):
    score_list = []
    for index, row in enumerate(test_data):

        article_id1, article_id2= row['SST_AIN_ID_1'], row['SST_AIN_ID_2']
        score = feature_filler.fill_score_map( article_id1, article_id2)

        logging.info("Score : {}".format(score))
        score_list.append(score)
        if (index % 100 == 0):
            logging.info("Processed {} rows".format(index))
    return score_list




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help='action can be create or append')
    parser.add_argument('--sincewhen', help='since when')
    args = parser.parse_args()

    config = yaml.safe_load(open('config.yml'))

    train_fail_loc = config["train_data_file"]
    test_fail_loc = config["test_data_file"]

    application = Application(config, True)
    feature_filler = FeatureFiller(articleLoader=application.articleLoader, summaryFacade=application.summaryFacade, tfidfFacade=application.tfidfFacade, doc2VecFacade=application.doc2VecFacade, classifierAggregator=application.classifierAggregator)
    application.gramFacade.load_phrases()
    if (args.action == 'train'):
        direct_confront(application, train_fail_loc, feature_filler)
    elif (args.action == 'test'):
        create_test_data(application, test_fail_loc, args.sincewhen)
