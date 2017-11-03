import logging
import os
import pickle
import sys
sys.path.append('..')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.generation import GramsGenerator

from technews_nlp_aggregator.nlp_model.publish import GramFacade


from datetime import datetime
import yaml

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))
models_dir = config["phrases_model_dir_base"] + datetime.now().isoformat()+'/'
def generate_model():

    os.mkdir(models_dir)

    pickle_file = config["text_pickle_file"]
    with open(pickle_file, 'rb') as f:
        texts = pickle.load(f)
        logging.info("Loaded {} texts".format(len(texts)))
        gramsGenerator = GramsGenerator( models_dir)
        gramsGenerator.create_model(texts)






    if os.path.islink(config["phrases_model_dir_link"]):
        os.unlink(config["phrases_model_dir_link"])

    os.symlink(models_dir,config["phrases_model_dir_link"])

def export_to_phrases():
    if not os.path.isdir(models_dir):
        os.mkdir(models_dir)
    pickle_dir = config["pickle_dir"]
    pickle_file = config["text_pickle_file"]
    bigrams_pickle_file = config["bigrams_pickle_file"]
    trigrams_pickle_file = config["trigrams_pickle_file"]

    phrase_model_dir = config["phrases_model_dir_link"]
    with open(pickle_file, 'rb') as f:
        texts = pickle.load(f)
        logging.info("Loaded {} texts".format(len(texts)))
        gramFacade = GramFacade(phrase_model_dir)
        bigrams = gramFacade.export_bigrams(texts)
        trigrams = gramFacade.export_trigrams(bigrams)
        logging.info("Saving {} texts as trigrams".format(len(trigrams)))
        bigrams_core_name, trigrams_core_name = 'bigrams_', 'trigrams_'
        bigrams_file = pickle_dir + bigrams_core_name + datetime.now().isoformat() + '.p'
        trigrams_file = pickle_dir + trigrams_core_name + datetime.now().isoformat() + '.p'


        with open(bigrams_file , 'wb') as f:
            pickle.dump(bigrams, f)

        with open(trigrams_file, 'wb') as f:
            pickle.dump(trigrams, f)

        if os.path.islink(config["bigrams_pickle_file"]):
            os.unlink(config["bigrams_pickle_file"])
        os.symlink(bigrams_file, config["bigrams_pickle_file"])

        if os.path.islink(config["trigrams_pickle_file"]):
            os.unlink(config["trigrams_pickle_file"])
        os.symlink(trigrams_file, config["trigrams_pickle_file"])


generate_model()
export_to_phrases()

def check_bigrams_trigrams():
    bigrams_pickle_file = config["bigrams_pickle_file"]
    trigrams_pickle_file = config["trigrams_pickle_file"]

    phrase_model_dir = config["phrases_model_dir_link"]
    with open(bigrams_pickle_file , 'rb') as f:
        bigrams = pickle.load(f)
    with open(trigrams_pickle_file , 'rb') as f:
        trigrams = pickle.load(f)

    print(bigrams[:50])
    print(trigrams[:50])

#check_bigrams_trigrams()