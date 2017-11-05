import sys
sys.path.append('..')
import yaml

from technews_nlp_aggregator.jobs import ArticleComparatorJob
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.common.util import daterange
from technews_nlp_aggregator.nlp_model.publish import TfidfFacade, Doc2VecFacade, GramFacade
from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer, TechArticlesWordTokenizer, defaultTokenizer
from datetime import datetime, date

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))
db_url    = db_config["db_url"]
articleDatasetRepo = ArticleDatasetRepo(db_url)
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)
gramFacade = GramFacade(config["phrases_model_dir_link"])

tfidfFacade = TfidfFacade(config["lsi_models_dir_link"], article_loader=articleLoader, gramFacade=gramFacade, tokenizer=defaultTokenizer)
tfidfFacade.load_models()

doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], article_loader=articleLoader, gramFacade=gramFacade, tokenizer=defaultTokenizer)
doc2VecFacade.load_models()

def find_with_model(model, thresholds,begin, finish, days_diff ):


    for start, end in daterange(begin, finish, days_diff):
        print(start.date(), end.date())
        articleComparatorJob = ArticleComparatorJob(db_url, model, thresholds)
        articleComparatorJob.find_articles(start.date(), end.date())


find_with_model(model = tfidfFacade, thresholds = (0.64, 0.995),
                begin = datetime(year=2017, month=1, day=1), finish = datetime(year=2017, month=11, day=3), days_diff=2)

find_with_model(model = doc2VecFacade, thresholds = (0.27, 0.99),
                begin = datetime(year=2017, month=1, day=1), finish = datetime(year=2017, month=11, day=3), days_diff=2)
