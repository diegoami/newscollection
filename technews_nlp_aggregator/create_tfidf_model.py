import logging
import os
import pickle
import sys
sys.path.append('..')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.generation import TfidfGenerator
from technews_nlp_aggregator.nlp_model.publish import  GramFacade



from datetime import datetime
import yaml

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))
models_dir = config["lsi_models_dir_base"] + datetime.now().isoformat()+'/'


os.mkdir(models_dir)

trigrams_file = config["trigrams_pickle_file"]
with open(trigrams_file , 'rb') as f:
    trigrams = pickle.load(f)
    logging.info("Loaded {} trigrams".format(len(trigrams)))
    tfidfGenerator = TfidfGenerator( models_dir)
    tfidfGenerator.create_model(trigrams)


if os.path.islink(config["lsi_models_dir_link"]):
    os.unlink(config["lsi_models_dir_link"])

os.symlink(models_dir,config["lsi_models_dir_link"])

