import logging
import pickle
import os
import sys
from datetime import datetime
from .application import Application
sys.path.append('..')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import yaml

def create_pickle(application ):
    _ = application
    pickle_dir = config["pickle_dir"]
    core_name = 'texts_'
    pickle_file = pickle_dir + core_name + datetime.now().isoformat() + '.p'
    logging.info("Articles loaded : {} ".format(len(_.articleLoader.articlesDF)))

    texts = _.tokenizer.tokenize_ddf(_.articleLoader.articlesDF)
    logging.info("Articles saved in pickle file : {} ".format(len(texts)))
    with open(pickle_file, 'wb') as f:
        pickle.dump(texts, f)
    if os.path.islink(config["text_pickle_file"]):
        os.unlink(config["text_pickle_file"])
    os.symlink(pickle_file, config["text_pickle_file"])

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    config = yaml.safe_load(open('../config.yml'))
    application = Application(config, True)

    create_pickle(application )




