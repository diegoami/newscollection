import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.model_common import ArticleLoader
from technews_nlp_aggregator.model_usage import Doc2VecFacade, TfidfFacade
import yaml


config = yaml.safe_load(open('../config.yml'))


articleLoader = ArticleLoader(listname=config["list_name"],dirname=config["parsed_articles_dir"])
articleLoader.load_articles_from_directory(True)
doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader)
doc2VecFacade.load_models()
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader)
tfidfFacade.load_models()

def print_articles(articles):
    for article in articles:
        print(article)






