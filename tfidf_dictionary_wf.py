import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import os
import pickle
import sys
from technews_nlp_aggregator.nlp_model.publish import TfidfGenerator
from technews_nlp_aggregator.common import load_config
from datetime import datetime
import yaml

DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'

def create_tfidf_model(config, param_config):
    db_config = yaml.safe_load(open(config["key_file"]))
    models_dir = config["root_dir"] + config["lsi_models_dir_base"] + datetime.now().isoformat()+'/'
    os.mkdir(models_dir)

    trigrams_file = config["root_dir"] + config["trigrams_pickle_file"]
    with open(trigrams_file , 'rb') as f:
        trigrams = pickle.load(f)
        logging.info("Loaded {} trigrams".format(len(trigrams)))
        tfidfGenerator = TfidfGenerator( models_dir, no_below=int(param_config['tdf_no_below']), no_above=float(param_config['tdf_no_above']) , num_topics=int(param_config['tdf_num_topics']), version=config['version'])
        corpus, dictionary = tfidfGenerator.create_dictionary(trigrams)




    if os.path.islink(config["root_dir"]+config["lsi_models_dir_link"]):
        os.unlink(config["root_dir"]+config["lsi_models_dir_link"])

    os.symlink(models_dir,config["root_dir"]+config["lsi_models_dir_link"])


if __name__ == '__main__':
    config = load_config(sys.argv)
    version = config['version']
    param_config = yaml.safe_load(open('v_' + str(version) + '.yml'))
    create_tfidf_model(config, param_config)
