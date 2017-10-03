import logging
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.model_common import ArticleLoader
from technews_nlp_aggregator.model_generation import Doc2VecGenerator
from datetime import datetime
import yaml


config = yaml.safe_load(open('config.yml'))
models_dir = config["doc2vec_models_dir_base"] + datetime.now().isoformat()+'/'

os.mkdir(models_dir)

articleLoader = ArticleLoader(listname=config["list_name"],dirname=config["parsed_articles_dir"])
articleLoader.load_articles_from_directory()
tfidfGenerator = Doc2VecGenerator(articleLoader.article_map, models_dir)
tfidfGenerator.create_model()

if os.path.islink(config["doc2vec_models_dir_link"]):
    os.unlink(config["doc2vec_models_dir_link"])
os.symlink(models_dir,config["doc2vec_models_dir_link"])
