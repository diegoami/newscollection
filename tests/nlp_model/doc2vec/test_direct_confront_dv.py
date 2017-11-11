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
        article_id1, article_id2= row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2']
        id1, id2 = _.articleLoader.get_id_from_article_id(article_id1), _.articleLoader.get_id_from_article_id(article_id2)
        article1, article2  = _.articleLoader.articlesDF.iloc[id1],  _.articleLoader.articlesDF.iloc[id2]
        score = _.doc2VecFacade.get_score_id_id(id1, id2)
        print(article_id1, article_id2, score)



if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    direct_confront(application)
