import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade
from technews_nlp_aggregator.nlp_model.publish.tdidf import FilterMatrixSimilarity

import yaml
from gensim import corpora, models, similarities

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.generation import TfidfGenerator

from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from datetime import datetime
import yaml
from datetime import date


config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader)
tfidfFacade.load_models()
#tfidfFacade.lsi.show_topics(num_topics=300, num_words=30, log=True)
print(type(tfidfFacade.index))
matrix = tfidfFacade.index
filterMatrix = FilterMatrixSimilarity(matrix)


end = date(2017, 10, 10)
start = date(2017, 10, 10)




docs_of_day = articleLoader.articles_in_interval(start, end)
dindex =  docs_of_day.index
articles_and_sim = {}
for id, row in docs_of_day.iterrows():
    vec_lsi = tfidfFacade.get_vec_docid(id)
    sims = filterMatrix[vec_lsi]
    for other_id in dindex:
        sim_score = sims[other_id]
        if (sim_score > 0.80 and id != other_id):
            articles_and_sim[(id, other_id)] = sim_score
for art_cp, score in articles_and_sim.items():
    id, other_id = art_cp
    article, otherarticle = articleLoader.articlesDF.loc[id], articleLoader.articlesDF.loc[other_id]
    print(article['title'], article['date_p'], otherarticle['title'], otherarticle['date_p'], score, sep=',')

