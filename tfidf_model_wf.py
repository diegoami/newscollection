import logging
import os
import pickle
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.nlp_model.publish import TfidfFacade
from datetime import datetime
import yaml


def create_tfidf_model(config):
    db_config = yaml.safe_load(open(config["key_file"]))
    models_dir = config["lsi_models_dir_base"] + datetime.now().isoformat()+'/'
    os.mkdir(models_dir)
    trigrams_dir = config["phrases_model_dir_link"]
    trigrams_file = trigrams_dir +'/' + 'trigrams_phraser'
    with open(trigrams_file , 'rb') as f:
        trigrams = pickle.load(f)

        logging.info("Loaded {} trigrams".format(len(trigrams)))
        tfidfFacade = TfidfFacade( models_dir)
        tfidfFacade.create_model(trigrams)


    if os.path.islink(config["lsi_models_dir_link"]):
        os.unlink(config["lsi_models_dir_link"])

    os.symlink(models_dir,config["lsi_models_dir_link"])


if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    create_tfidf_model(config)