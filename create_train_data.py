

import yaml
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.application import Application
import argparse
def direct_confront(application, train_file):
    _ = application

    user_paired = _.similarArticlesRepo.retrieve_user_paired()

    scores = retrieves_scores(_, user_paired)
    df = pd.DataFrame(scores)
    print(df.head())
    df.to_csv(train_file)

def create_test_data(application):

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
        logging.info("Score : {}".format(score))
        score_list.append(score)
        if (index % 100 == 0):
            logging.info("Processed {} rows".format(index))
    return score_list


def retrieves_test(_, test_data):
    score_list = []
    for index, row in enumerate(test_data):

        article_id1, article_id2= row['SST_AIN_ID_1'], row['SST_AIN_ID_2']
        score = fill_score_map(_, article_id1, article_id2)

        logging.info("Score : {}".format(score))
        score_list.append(score)
        if (index % 100 == 0):
            logging.info("Processed {} rows".format(index))
    return score_list

def fill_score_map(_, article_id1, article_id2):
    id1, id2 = _.articleLoader.get_id_from_article_id(article_id1), _.articleLoader.get_id_from_article_id(
        article_id2)
    article1, article2 = _.articleLoader.articlesDF.iloc[id1], _.articleLoader.articlesDF.iloc[id2]
    summary1, summary2 = _.summaryFacade.full_text_summarize(id1,article1['text'], article1['title'], 0.85 ), \
                         _.summaryFacade.full_text_summarize(id2, article2['text'],  article2['title'], 0.85 )
    summary1b, summary2b = _.summaryFacade.full_text_summarize(id1, article1['text'], article1['title'], 0.7), \
                         _.summaryFacade.full_text_summarize(id2, article2['text'], article2['title'], 0.7)

    score = {}
    score["SCO_AIN_ID_1"], score["SCO_AIN_ID_2"] = article_id1, article_id2
    score["SCO_T_TEXT"], score["SCO_T_TITLE"], score["SCO_T_SUMMARY"], score["SCO_T_SUMMARY_2"]  = scores_from_classifiers(_.tfidfFacade, article1,
                                                                                                article2, id1, id2,
                                                                                                summary1, summary2, summary1b, summary2b)
    score["SCO_D_TEXT"], score["SCO_D_TITLE"], score["SCO_D_SUMMARY"], score["SCO_D_SUMMARY_2"] = scores_from_classifiers(_.doc2VecFacade,
                                                                                                article1, article2,
                                                                                                id1, id2, summary1,
                                                                                                summary2, summary1b, summary2b)

    score["SCO_CW_TEXT"], score["SCO_CW_TITLE"], score["SCO_CW_SUMMARY"], score["SCO_CW_SUMMARY_2"] =     unique_words_diff(_.classifierAggregator,
                                                                                                          article1,
                                                                                                          article2,
                                                                                                          id1, id2,
                                                                                                          summary1,
                                                                                                          summary2,
                                                                                                          summary1b,
                                                                                                          summary2b
                                                                                                          )
    score["SCO_DAYS"] = abs((article2['date_p'] - article1['date_p']).days)
    logging.info(article1['title'])
    logging.info(article2['title'])

    return score


def scores_from_classifiers(classifier, article1, article2, id1, id2, summary1, summary2, summary1b, summary2b):
    score = classifier.get_score_id_id(id1, id2)
    score_tit = classifier.get_score_doc_doc(article1['title'], article2['title'])
    score_sum = classifier.get_score_doc_doc(article1["title"]+ ".\n "+summary1, article2["title"]+ ".\n "+summary2)
    score_sum_b = classifier.get_score_doc_doc(article1["title"]+ ".\n "+summary1b, article2["title"]+ ".\n "+summary2b)
    return score, score_tit, score_sum, score_sum_b


def unique_words_diff(aggregator, article1, article2, id1, id2, summary1, summary2, summary1b, summary2b):
    cw_tot = aggregator.common_miss_words_doc(article1["title"]+ ".\n "+article1["text"], article2["title"]+ ".\n "+article2["text"])
    cw_tit = aggregator.common_miss_words_doc(article1['title'], article2['title'])
    cw_sum1 = aggregator.common_miss_words_doc(article1["title"]+ ".\n "+summary1, article2["title"]+ ".\n "+summary2)
    cw_sum_b = aggregator.common_miss_words_doc(article1["title"]+ ".\n "+summary1b, article2["title"]+ ".\n "+summary2b)
    return cw_tot, cw_tit, cw_sum1, cw_sum_b


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help='action can be create or append')
    args = parser.parse_args()

    config = yaml.safe_load(open('config.yml'))
    train_fail_loc = config["train_data_file"]
    application = Application(config, True)
    application.gramFacade.load_phrases()
    if (args.action == 'train'):
        direct_confront(application,train_fail_loc)
    elif (args.action == 'test'):
        create_test_data(application)
