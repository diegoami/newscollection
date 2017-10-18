import time

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade
import yaml


from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.generation import TfidfGenerator
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from datetime import datetime
import yaml

config = yaml.safe_load(open('../../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(load_text=True)
doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader)
doc2VecFacade.load_models()
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader)
tfidfFacade.load_models()







def print_articles(articles):
    for article in articles:
        print(article)

print(articleLoader.articlesDF.head())
while True:
    #random_article_id, random_article=  articleLoader.get_random_article()
    #random_article_id = random_article.index[0]
    random_article_id = 15073
    print(articleLoader.articlesDF.loc[random_article_id])
    #print(random_article)
    print(" ============= ARTICLE ==================")

    print(" ============= DOC2VEC ==================")
    articles1 = doc2VecFacade.find_related_articles( random_article_id)
    print(articles1)
    print(" ============= TFIDF==================")

    articles2 = tfidfFacade.find_related_articles( random_article_id)
    print(articles2)
    time.sleep(0.75)