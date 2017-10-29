import logging
import pickle
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer, TechArticlesTokenExcluder, SimpleTokenExcluder
from datetime import datetime


import yaml

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))
pickle_dir = config["pickle_dir"]


def create_pickle(withTexts=True):
    articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
    articleLoader = ArticleLoader(articleDatasetRepo)
    articleLoader.load_all_articles(load_text=withTexts, load_meta=False)
    tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer(),
                                 token_excluder=TechArticlesTokenExcluder())
    core_name = 'texts_'
    pickle_file = pickle_dir + core_name + datetime.now().isoformat() + '.p'
    texts = tokenizer.tokenize_ddf(articleLoader.articlesDF)
    with open(pickle_file, 'wb') as f:
        pickle.dump(texts, f)
    if os.path.islink(config["text_pickle_file"]):
        os.unlink(config["text_pickle_file"])
    os.symlink(pickle_file, config["text_pickle_file"])


create_pickle()
