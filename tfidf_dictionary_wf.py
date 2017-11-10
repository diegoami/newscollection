import logging
import os
import pickle

from technews_nlp_aggregator.nlp_model.publish import TfidfGenerator
from datetime import datetime
import yaml

DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'

def create_tfidf_model(config):
    db_config = yaml.safe_load(open(config["key_file"]))
    models_dir = config["lsi_models_dir_base"] + datetime.now().isoformat()+'/'
    os.mkdir(models_dir)

    trigrams_file = config["trigrams_pickle_file"]
    with open(trigrams_file , 'rb') as f:
        trigrams = pickle.load(f)
        logging.info("Loaded {} trigrams".format(len(trigrams)))
        tfidfGenerator = TfidfGenerator( models_dir)
        corpus, dictionary = tfidfGenerator.create_dictionary(trigrams)




    if os.path.islink(config["lsi_models_dir_link"]):
        os.unlink(config["lsi_models_dir_link"])

    os.symlink(models_dir,config["lsi_models_dir_link"])


if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    create_tfidf_model(config)