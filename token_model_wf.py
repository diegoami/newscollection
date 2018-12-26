import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import pickle
import os
from technews_nlp_aggregator.common import load_config
import sys
from datetime import datetime

import yaml
from technews_nlp_aggregator.persistence import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, defaultTokenizer
from technews_nlp_aggregator.common import load_config

import argparse


def create_pickle( config , articleLoader, tokenizer, limit=None):

    logging.info("Articles loaded : {} ".format(len(articleLoader.articlesDF)))
    articleFilterDF = articleLoader.articlesDF[:limit] if limit else articleLoader.articlesDF
    texts_df = tokenizer.tokenize_ddf(articleFilterDF )
    texts = texts_df.tolist()
    if (not limit):
        save_picke_file(config, texts)


def save_picke_file(config, texts):
    core_name = 'texts_'
    pickle_file = config["root_dir"]+config["pickle_dir"] + core_name + datetime.now().isoformat() + '.p'

    logging.info("Articles saved in pickle file : {} ".format(len(texts)))
    with open(pickle_file, 'wb') as f:
        pickle.dump(texts, f)
    if os.path.islink(config["root_dir"]+config["text_pickle_file"]):
        os.unlink(config["root_dir"]+config["text_pickle_file"])
    os.symlink(pickle_file, config["root_dir"]+config["text_pickle_file"])


def update_pickle(config, articleLoader, tokenizer):

    pickle_file = config["root_dir"]+config["text_pickle_file"]
    texts = []
    if not os.path.isfile(pickle_file):
        logging.error("File {} not found".format(pickle_file))
        logging.error("Change action to create")
        exit(1)
    with open(pickle_file, 'rb') as f:
        texts = pickle.load(f)
    logging.info("Loaded {} texts".format(len(texts)))
    logging.info("Articles loaded : {} ".format(len(articleLoader.articlesDF)))
    last_texts = texts[-10:]
    for index, last_text in enumerate(last_texts):
        logging.info("=============== {} ===================".format(len(texts)-9+index))
        logging.info(last_text)

    articlesNewDF = articleLoader.articlesDF
    new_textsDF =  tokenizer.tokenize_ddf(articlesNewDF )
    new_texts = new_textsDF.tolist()

    texts = texts + new_texts
    save_picke_file(config, texts)


if __name__ == '__main__':

    config = load_config(sys.argv)
    action = config['tok_action']
    db_config = yaml.safe_load(open(config["key_file"]))
    db_url = db_config["db_url"]
    articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"))
    logging.info("DB_URL: {}".format(db_config.get("db_url")))
    articleLoader = ArticleLoader(articleDatasetRepo)
    logging.info("Loading articles....")
    if not os.path.isdir(config["root_dir"] + config["pickle_dir"]):
        os.mkdir(config["root_dir"] + config["pickle_dir"])

    if (action == 'append'):
        logging.info("Appending....")
        articleLoader.load_all_articles(load_text=True, load_only_unsaved=True)
        logging.info("Finished loading articles....")
        update_pickle(config, articleLoader, defaultTokenizer)
        articleDatasetRepo.update_to_saved()
    elif (action  == 'create'):
        logging.info("Creating new pickle file....")
        articleLoader.load_all_articles(load_text=True, load_only_unsaved=False)
        logging.info("Finished loading articles....")
        create_pickle(config, articleLoader, defaultTokenizer)
        articleDatasetRepo.update_to_saved()

    else:
        print("Please choose create or append for tok_action")
        sys.exit(1)



