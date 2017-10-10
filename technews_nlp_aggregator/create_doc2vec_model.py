import logging
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.generation import Doc2VecGenerator
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from datetime import datetime
import yaml


config = yaml.safe_load(open('../config.yml'))

articleDatasetRepo = ArticleDatasetRepo(config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles()
models_dir = config["doc2vec_models_dir_base"] + datetime.now().isoformat()+'/'

os.mkdir(models_dir)

tfidfGenerator = Doc2VecGenerator(articleLoader.article_map, models_dir)
tfidfGenerator.create_model()

if os.path.islink(config["doc2vec_models_dir_link"]):
    os.unlink(config["doc2vec_models_dir_link"])
os.symlink(models_dir,config["doc2vec_models_dir_link"])
