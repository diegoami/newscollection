from technews_nlp_aggregator.jobs import ArticleComparatorJob
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.common.util import daterange
from technews_nlp_aggregator.nlp_model.publish import TfidfFacade, Doc2VecFacade
from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from datetime import datetime, date
import yaml

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))
db_url    = db_config["db_url"]
articleDatasetRepo = ArticleDatasetRepo(db_url)
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)
tfidfFacade = TfidfFacade(config["lsi_models_dir_link"], articleLoader)
tfidfFacade.load_models()

doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader)
doc2VecFacade.load_models()

def find_with_model(model, thresholds,begin, finish ):


    for start, end in daterange(begin, finish):
        print(start.date(), end.date())
        articleComparatorJob = ArticleComparatorJob(db_url, model, thresholds)
        articleComparatorJob.find_articles(start.date(), end.date())


#find_with_model(model = tfidfFacade, thresholds = (0.74, 0.75),
#                begin = datetime(year=2017, month=3, day=1), finish = datetime(year=2017, month=10, day=21))

find_with_model(model = doc2VecFacade, thresholds = (0.44, 0.48),
                begin = datetime(year=2017, month=3, day=1), finish = datetime(year=2017, month=10, day=21))
