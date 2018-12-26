import os
import pickle
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade
from technews_nlp_aggregator.common import load_config
from datetime import datetime
import yaml
import sys

def create_doc2vec_model(config, param_config):
    db_config = yaml.safe_load(open(config["key_file"]))
    pickle_dir = config["root_dir"]+config["pickle_dir"]

    models_dir = config["root_dir"]+config["doc2vec_models_dir_base"] + datetime.now().isoformat()+'/'
    os.makedirs(models_dir, exist_ok=True)

    pickle_file = config["root_dir"]+config["trigrams_pickle_file"]
    with open(pickle_file, 'rb') as f:
        trigrams = pickle.load(f)
        doc2VecFacade = Doc2VecFacade( models_dir, min_count=int(param_config['docvec_min_count']), window=int(param_config['docvec_window']),
                                       sample=float(param_config['docvec_sample']), epochs=int(param_config['docvec_epochs']), alpha=float(param_config['docvec_alpha']),                       vector_size=int(param_config['docvec_vector_size']), batch_size=int(param_config['docvec_batch_size']),
                                       queue_factor=int(param_config['docvec_queue_factor']), workers=int(param_config['docvec_workers']),
                                       version=config['version']              )

        doc2VecFacade.create_model(trigrams)

    if os.path.islink(config["root_dir"]+config["doc2vec_models_dir_link"]):
        os.unlink(config["root_dir"]+config["doc2vec_models_dir_link"])
    os.symlink(models_dir,config["root_dir"]+config["doc2vec_models_dir_link"])

if __name__ == '__main__':
    config = load_config(sys.argv)
    version = config['version']
    param_config = yaml.safe_load(open('v_' + str(version) + '.yml'))
    create_doc2vec_model(config, param_config)