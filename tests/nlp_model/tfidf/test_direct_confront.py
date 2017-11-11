import logging

from gensim import similarities

import yaml
from datetime import date
from technews_nlp_aggregator.application import Application

config = yaml.safe_load(open('../../../config.yml'))
def direct_confront(_, n_articles=5):
    _ = application

    user_paired = _.similarArticlesRepo.retrieve_user_paired()
    for row in user_paired:
        article_id1, article_id2, similarity = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2'], row['SSU_SIMILARITY']
        id1, id2 = _.articleLoader.get_id_from_article_id(article_id1), _.articleLoader.get_id_from_article_id(article_id2)
        article1, article2  = _.articleLoader.articlesDF.iloc[id1],  _.articleLoader.articlesDF.iloc[id2]
        score, score_tit, score_tit_tex1, score_tit_tex2 = scores_from_classifiers(_.tfidfFacade, article1, article2, id1, id2)
        print('T:', article_id1, article_id2, score, score_tit, score_tit_tex1, score_tit_tex2, similarity)
        score, score_tit, score_tit_tex1, score_tit_tex2 = scores_from_classifiers(_.doc2VecFacade, article1, article2,
                                                                                   id1, id2)
        print('D:', article_id1, article_id2, score, score_tit, score_tit_tex1, score_tit_tex2, similarity)


def scores_from_classifiers(classifier, article1, article2, id1, id2):
    score = classifier.get_score_id_id(id1, id2)
    score_tit = classifier.get_score_doc_doc(article1['title'], article2['title'])
    score_tit_tex1 = classifier.get_score_doc_doc(article1['title'], article1['title'] + ".\n " + article1['text'])
    score_tit_tex2 = classifier.get_score_doc_doc(article2['title'], article2['title'] + ".\n " + article2['text'])
    return score, score_tit, score_tit_tex1, score_tit_tex2


if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    direct_confront(application)
