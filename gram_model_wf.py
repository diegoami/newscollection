import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import os
import pickle



from technews_nlp_aggregator.nlp_model.publish import GramFacade
from datetime import datetime
import yaml




def generate_model(config):

    models_dir =  config["root_dir"]+config["phrases_model_dir_base"] + datetime.now().isoformat() + '/'
    os.mkdir(models_dir)


    pickle_file = config["root_dir"]+config["text_pickle_file"]
    with open(pickle_file, 'rb') as f:
        texts = pickle.load(f)
        logging.info("Loaded {} texts".format(len(texts)))
        gramFacade = GramFacade(models_dir)
        gramFacade.create_model(texts)
    if os.path.islink(config["root_dir"]+config["phrases_model_dir_link"]):
        os.unlink(config["root_dir"]+config["phrases_model_dir_link"])

    os.symlink(models_dir, config["root_dir"]+config["phrases_model_dir_link"])



if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))
    generate_model(config)

