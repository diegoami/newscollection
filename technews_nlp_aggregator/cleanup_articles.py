import sys
sys.path.append('..')
import yaml

from technews_nlp_aggregator.jobs import ArticleComparatorJob
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.common.util import daterange
from technews_nlp_aggregator.nlp_model.publish import TfidfFacade, Doc2VecFacade
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer, TechArticlesTokenExcluder, SimpleTokenExcluder, NltkWordTokenizer
from datetime import datetime, date


config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))
db_url    = db_config["db_url"]
articleDatasetRepo = ArticleDatasetRepo(db_url)
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)

tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer(),
                                 token_excluder=TechArticlesTokenExcluder(),
                             word_tokenizer=NltkWordTokenizer())

