import logging
import os
import pickle

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.generation import TfidfGenerator




from datetime import datetime
import yaml

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))
models_dir = config["lsi_models_dir_base"] + datetime.now().isoformat()+'/'


os.mkdir(models_dir)

pickle_file = config["text_pickle_file"]
with open(pickle_file, 'rb') as f:
    texts = pickle.load(f)
    tfidfGenerator = TfidfGenerator( models_dir)
    tfidfGenerator.create_model(texts)


if os.path.islink(config["lsi_models_dir_link"]):
    os.unlink(config["lsi_models_dir_link"])

os.symlink(models_dir,config["lsi_models_dir_link"])

