import logging
import pickle
import os
import sys
sys.path.append('..')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo


import yaml

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleDatasetRepo.delete_short_texts()