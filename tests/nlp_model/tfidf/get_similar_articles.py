import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import similarities

import yaml
from datetime import date
from technews_nlp_aggregator.application import Application

config = yaml.safe_load(open('../../../config.yml'))

def compare_articles(application, start, end):
    _ = application
    matrix = _.tfidfFacade.matrix_wrapper.similarityMatrix
    otherMatrix = similarities.MatrixSimilarity(corpus = None, num_features=matrix.num_features, corpus_len=len(matrix.index))
    otherMatrix.num_features = matrix.num_features
    otherMatrix.num_best = matrix.num_best
    otherMatrix.normalize = True
    otherMatrix.chunksize = matrix.chunksize
    otherMatrix.index = matrix

    start = date(2017, 10, 10)
    end = date(2017, 10, 11)

    articles_Found = _.tfidfFacade.compare_articles_from_dates(start, end,(.75,.995))
    for id, sims in articles_Found.items():
        for other_id, score in sims:
            article, otherarticle = _.articleLoader.articlesDF.iloc[id], _.articleLoader.articlesDF.iloc[other_id]
            article_id, article_other_id = article['article_id'], otherarticle['article_id']
            print(" ============================================== ")
            print(article)
            print(" ============================================== ")
            print(otherarticle)


if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    compare_articles(application, date(2017, 10, 10), date(2017, 10, 11))

