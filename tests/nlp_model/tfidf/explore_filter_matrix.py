import logging

from technews_nlp_aggregator.nlp_model.publish.tdidf import FilterMatrixSimilarity
from datetime import date
import yaml
from technews_nlp_aggregator.application import Application
#tfidfFacade.lsi.show_topics(num_topics=300, num_words=30, log=True)
def test_filter_matrix(application, start, end):
    _ = application

    matrix = _.tfidfFacade.matrix_wrapper.similarityMatrix
    filterMatrix = FilterMatrixSimilarity(matrix)


    end = date(2017, 10, 10)
    start = date(2017, 10, 10)




    docs_of_day = _.articleLoader.articles_in_interval(start, end)
    dindex =  docs_of_day.index
    articles_and_sim = {}
    for id, row in docs_of_day.iterrows():
        vec_lsi = _.tfidfFacade.get_vec_docid(id)
        sims = filterMatrix[vec_lsi]
        for other_id in dindex:
            sim_score = sims[other_id]
            if (sim_score > 0.80 and id != other_id):
                articles_and_sim[(id, other_id)] = sim_score
    for art_cp, score in articles_and_sim.items():
        id, other_id = art_cp
        article, otherarticle = _.articleLoader.articlesDF.loc[id], _.articleLoader.articlesDF.loc[other_id]
        print(article['title'], article['date_p'], otherarticle['title'], otherarticle['date_p'], score, sep=',')


if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    test_filter_matrix(application, date(2017, 10, 10), date(2017, 10, 11))

