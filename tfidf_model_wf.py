import logging
import os
import pickle
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.nlp_model.publish import TfidfGenerator
from datetime import datetime
import yaml


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
        del trigrams
        lsi = tfidfGenerator.create_model(corpus, dictionary)



    if os.path.islink(config["lsi_models_dir_link"]):
        os.unlink(config["lsi_models_dir_link"])

    os.symlink(models_dir,config["lsi_models_dir_link"])


if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    create_tfidf_model(config)