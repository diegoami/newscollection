import logging

from gensim import similarities

import yaml
from datetime import date
from technews_nlp_aggregator.application import Application


def retrieve_scores(application, n_articles=25):
    _ = application

    for i in range(n_articles):
        index, article = _.articleLoader.get_random_article()
        article_id = article['article_id']
        articles_similar = _.classifierAggregator.retrieve_articles_for_id(index, 3, 25, 0)
        print(articles_similar)

if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    retrieve_scores(application)
