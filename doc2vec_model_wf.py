import os
import pickle
import logging


from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade

from datetime import datetime
import yaml

def create_doc2vec_model(config):
    db_config = yaml.safe_load(open(config["key_file"]))
    pickle_dir = config["pickle_dir"]

    models_dir = config["doc2vec_models_dir_base"] + datetime.now().isoformat()+'/'
    os.mkdir(models_dir)

    pickle_file = config["trigrams_pickle_file"]
    with open(pickle_file, 'rb') as f:
        trigrams = pickle.load(f)
        doc2VecFacade = Doc2VecFacade( models_dir)

        doc2VecFacade.create_model(trigrams)

    if os.path.islink(config["doc2vec_models_dir_link"]):
        os.unlink(config["doc2vec_models_dir_link"])
    os.symlink(models_dir,config["doc2vec_models_dir_link"])

if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))
    create_doc2vec_model(config)