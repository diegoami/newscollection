import logging
import os
import pickle

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.generation import Doc2VecGenerator
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer, TechArticlesTokenExcluder, SimpleTokenExcluder
from datetime import datetime


import yaml

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))
pickle_dir = config["pickle_dir"]

models_dir = config["doc2vec_models_dir_base"] + datetime.now().isoformat()+'/'
os.mkdir(models_dir)

pickle_file = config["text_pickle_file"]
with open(pickle_file, 'rb') as f:
    texts = pickle.load(f)
    doc2VecGenerator = Doc2VecGenerator( models_dir)

    doc2VecGenerator.create_model(texts)
    doc2VecGenerator.train_model()

if os.path.islink(config["doc2vec_models_dir_link"]):
    os.unlink(config["doc2vec_models_dir_link"])
os.symlink(models_dir,config["doc2vec_models_dir_link"])
