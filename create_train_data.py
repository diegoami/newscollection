

import yaml
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.application import Application
from technews_nlp_aggregator.prediction import FeatureFiller
import argparse
def direct_confront(train_file, feature_filler, similarArticlesRepo):


    user_paired = similarArticlesRepo.retrieve_user_paired()

    scores = retrieves_scores(user_paired, feature_filler, similarArticlesRepo)
    df = pd.DataFrame(scores)
    print(df.head())
    df.to_csv(train_file)


def retrieves_scores(user_paired, feature_filler, similarArticlesRepo):
    score_list = []
    con = similarArticlesRepo.get_connection()
    for index, row in enumerate(user_paired):
        article_id1, article_id2, similarity = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2'],  row['SSU_SIMILARITY']
        score = feature_filler.fill_score_map( article_id1, article_id2)
        similarArticlesRepo.insert_score(score, con)
        score["SCO_USER"] = similarity
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


