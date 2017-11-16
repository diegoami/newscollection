import logging

from gensim import similarities

import yaml
from datetime import date
import pandas as pd
from pandas import DataFrame

from technews_nlp_aggregator.application import Application

config = yaml.safe_load(open('../../../config.yml'))
def direct_confront(_, n_articles=5):
    _ = application

    user_paired = _.similarArticlesRepo.retrieve_user_paired()

    iterate_scores(_, user_paired)


def iterate_scores(_, user_paired):
    for row in user_paired:
        article_id1, article_id2, similarity = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2'], row['SSU_SIMILARITY']
        id1, id2 = _.articleLoader.get_id_from_article_id(article_id1), _.articleLoader.get_id_from_article_id(
            article_id2)
        article1, article2 = _.articleLoader.articlesDF.iloc[id1], _.articleLoader.articlesDF.iloc[id2]

        summary1, summary2 = _.summaryFacade.summarize(id1, article1['text']), _.summaryFacade.summarize(id2, article2[
            'text'])
        _.summaryFacade.summarize(id1, article1['text'])

        score_T, score_tit_T, score_sum_T = scores_from_classifiers(_.tfidfFacade, article1, article2, id1, id2,
                                                                    summary1, summary2)
        score_D, score_tit_D, score_sum_D = scores_from_classifiers(_.doc2VecFacade, article1, article2,
                                                                    id1, id2)
        d_days = abs(article2['date_p'].dt.days - article1['date_p'].dt.days)
        yield


def scores_from_classifiers(classifier, article1, article2, id1, id2, summary1, summary2):
    score = classifier.get_score_id_id(id1, id2)
    score_tit = classifier.get_score_doc_doc(article1['title'], article2['title'])
    score_sum = classifier.get_score_doc_doc(summary1, summary2)
    return score, score_tit,


if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    direct_confront(application)
