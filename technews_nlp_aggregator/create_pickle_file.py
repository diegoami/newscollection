import logging
import pickle
import os
import sys
sys.path.append('..')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer,  TechArticlesWordTokenizer, defaultTokenizer
from datetime import datetime


import yaml

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))
pickle_dir = config["pickle_dir"]
articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"], db_config.get("limit", None))
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(load_text=True)


def create_pickle(tokenizer):
    core_name = 'texts_'
    pickle_file = pickle_dir + core_name + datetime.now().isoformat() + '.p'
    logging.info("Articles loaded : {} ".format(len(articleLoader.articlesDF)))

    texts = defaultTokenizer.tokenize_ddf(articleLoader.articlesDF)
    logging.info("Articles saved in pickle file : {} ".format(len(texts)))
    with open(pickle_file, 'wb') as f:
        pickle.dump(texts, f)
    if os.path.islink(config["text_pickle_file"]):
        os.unlink(config["text_pickle_file"])
    os.symlink(pickle_file, config["text_pickle_file"])

tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer(),
                             word_tokenizer=TechArticlesWordTokenizer())
create_pickle( tokenizer=tokenizer)
#create_phrases( tokenizer=tokenizer)



def create_phrases(tokenizer):
    pickle_file = config["text_pickle_file"]

    with open(pickle_file, 'rb') as f:
        texts = pickle.load(f)
    core_name = 'phrases_'
    phrases_file = pickle_dir + core_name + datetime.now().isoformat() + '.p'
    phrases = tokenizer.word_tokenizer.phrase_doc_list(texts)
    with open(pickle_file, 'wb') as f:
        pickle.dump(phrases , f)
    if os.path.islink(config["phrases_pickle_file"]):
        os.unlink(config["phrases_pickle_file"])
    os.symlink(pickle_file, config["phrases_pickle_file"])





