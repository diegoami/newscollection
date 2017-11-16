

import yaml
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.application import Application
import argparse
def direct_confront(_):
    _ = application

    user_paired = _.similarArticlesRepo.retrieve_user_paired()

    scores = retrieves_scores(_, user_paired)
    df = pd.DataFrame(scores)
    print(df.head())
    df.to_csv('data/scores.csv')
def create_test_data(_):

    _ = application

    test_data = _.similarArticlesRepo.retrieve_similar_since('2017-11-01')
    logging.info("Retrieved {} ".format(len(test_data)))
    test  = retrieves_test(_, test_data )

    df = pd.DataFrame(test )
    print(df.head())
    df.to_csv('data/test.csv')


def retrieves_scores(_, user_paired):
    score_list = []
    for index, row in enumerate(user_paired):

        article_id1, article_id2, similarity = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2'],  row['SSU_SIMILARITY']
        score = fill_score_map(_, article_id1, article_id2)
        score["SCO_USER"] = similarity
        score_list.append(score)
        if (index % 100 == 0):
            logging.info("Processed {} rows".format(index))
    return score_list


def retrieves_test(_, test_data):
    score_list = []
    for index, row in enumerate(test_data):

        article_id1, article_id2= row['SST_AIN_ID_1'], row['SST_AIN_ID_2']
        score = fill_score_map(_, article_id1, article_id2)
        score_list.append(score)
        if (index % 100 == 0):
            logging.info("Processed {} rows".format(index))
    return score_list

def fill_score_map(_, article_id1, article_id2):
    id1, id2 = _.articleLoader.get_id_from_article_id(article_id1), _.articleLoader.get_id_from_article_id(
        article_id2)
    article1, article2 = _.articleLoader.articlesDF.iloc[id1], _.articleLoader.articlesDF.iloc[id2]
    summary1, summary2 = _.summaryFacade.full_text_summarize(id1,
                                                             article1['text']), _.summaryFacade.full_text_summarize(id2,
                                                                                                                    article2[
                                                                                                                        'text'])
    score = {}
    score["SCO_AIN_ID_1"], score["SCO_AIN_ID_2"] = article_id1, article_id2
    score["SCO_T_TEXT"], score["SCO_T_TITLE"], score["SCO_T_SUMMARY"] = scores_from_classifiers(_.tfidfFacade, article1,
                                                                                                article2, id1, id2,
                                                                                                summary1, summary2)
    score["SCO_D_TEXT"], score["SCO_D_TITLE"], score["SCO_D_SUMMARY"] = scores_from_classifiers(_.doc2VecFacade,
                                                                                                article1, article2,
                                                                                                id1, id2, summary1,
                                                                                                summary2)
    score["SCO_DAYS"] = abs((article2['date_p'] - article1['date_p']).days)
    return score


def scores_from_classifiers(classifier, article1, article2, id1, id2, summary1, summary2):
    score = classifier.get_score_id_id(id1, id2)
    score_tit = classifier.get_score_doc_doc(article1['title'], article2['title'])
    score_sum = classifier.get_score_doc_doc(summary1, summary2)
    return score, score_tit, score_sum


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    config = yaml.safe_load(open('config.yml'))
    application = Application(config, True)
   # direct_confront(application)
    create_test_data(application)
