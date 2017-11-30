import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import pickle
import os

import sys
from datetime import datetime

import yaml
from technews_nlp_aggregator.persistence import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, defaultTokenizer
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
    with open(pickle_file, 'rb') as f:
        texts = pickle.load(f)
        logging.info("Loaded {} texts".format(len(texts)))
        logging.info("Articles loaded : {} ".format(len(articleLoader.articlesDF)))


        articlesNewDF = articleLoader.articlesDF
        new_textsDF =  tokenizer.tokenize_ddf(articlesNewDF )
        new_texts = new_textsDF.tolist()

        texts = texts + new_texts
        save_picke_file(config, texts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help='action can be create or append')
    args = parser.parse_args()

    config = yaml.safe_load(open('config.yml'))
    db_config = yaml.safe_load(open(config["root_dir"]+config["key_file"]))
    db_url = db_config["db_url"]
    articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"))
    articleLoader = ArticleLoader(articleDatasetRepo)
    logging.info("Loading articles....")

    if (args.action == 'append'):
        logging.info("Appending....")
        articleLoader.load_all_articles(load_text=True, load_only_unsaved=True)
        logging.info("Finished loading articles....")
        update_pickle(config, articleLoader, defaultTokenizer)
        articleDatasetRepo.update_to_saved()
    elif (args.action == 'create'):
        logging.info("Creating new pickle file....")
        articleLoader.load_all_articles(load_text=True, load_only_unsaved=False)
        logging.info("Finished loading articles....")
        create_pickle(config, articleLoader, defaultTokenizer)
        articleDatasetRepo.update_to_saved()

    else:
        print("Please choose create or append")
        sys.exit(1)



