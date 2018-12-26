import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import os
import pickle



from technews_nlp_aggregator.nlp_model.publish import GramFacade
from technews_nlp_aggregator.common import load_config
from datetime import datetime
import yaml
import sys



def generate_model(config, param_config ):

    models_dir =  config["root_dir"]+config["phrases_model_dir_base"] + datetime.now().isoformat() + '/'

    os.makedirs(models_dir, exist_ok=True)


    pickle_file = config["root_dir"]+config["text_pickle_file"]
    with open(pickle_file, 'rb') as f:
        texts = pickle.load(f)
        logging.info("Loaded {} texts".format(len(texts)))
        gramFacade = GramFacade(models_dir, bigrams_threshold=float(param_config["bigrams_threshold"]), trigrams_threshold=float(param_config["trigrams_threshold"]))
        gramFacade.create_model(texts)
    if os.path.islink(config["root_dir"]+config["phrases_model_dir_link"]):
        os.unlink(config["root_dir"]+config["phrases_model_dir_link"])

    os.symlink(models_dir, config["root_dir"]+config["phrases_model_dir_link"])



if __name__ == '__main__':
    config = load_config(sys.argv)
    version = config['version']
    param_config = yaml.safe_load(open('v_'+str(version)+'.yml'))
    generate_model(config, param_config )

