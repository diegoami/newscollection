import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade
import yaml
from gensim import corpora, models, similarities

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.generation import TfidfGenerator
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from datetime import datetime
import yaml
from datetime import date


config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader)
tfidfFacade.load_models()
#tfidfFacade.lsi.show_topics(num_topics=300, num_words=30, log=True)
print(type(tfidfFacade.index))
matrix = tfidfFacade.index
otherMatrix = similarities.MatrixSimilarity(corpus = None, num_features=matrix.num_features, corpus_len=len(matrix.index))

otherMatrix.num_features = matrix.num_features
otherMatrix.num_best = matrix.num_best
otherMatrix.normalize = True
otherMatrix.chunksize = matrix.chunksize
otherMatrix.index = matrix.index

start = date(2017, 10, 10)

end = date(2017, 10, 11)


articles_Found = tfidfFacade.compare_articles_from_dates(start, end,(.75,.995))
for art_cp, score in articles_Found.items():
    id, other_id = art_cp
    article, otherarticle = articleLoader.articlesDF.loc[id], articleLoader.articlesDF.loc[other_id]
    print(article['date_p'], otherarticle['date_p'], article['title'], otherarticle['title'], score, sep=',')


"""
docs_of_day = articleLoader.articles_in_interval(start, end)
articles_and_sim = {}
for id, row in docs_of_day.iterrows():
    vec_lsi = tfidfFacade.get_vec_docid(id)
    sims = otherMatrix[vec_lsi]
    for other_id, sim_score in enumerate(sims):
        if (sim_score > 0.80 and id != other_id):
            articles_and_sim[(id, other_id)] = sim_score
for art_cp, score in articles_and_sim.items():
    id, other_id = art_cp
    article, otherarticle = articleLoader.articlesDF.loc[id], articleLoader.articlesDF.loc[other_id]
    print(article['title'], otherarticle['title'], score, sep=',')

"""