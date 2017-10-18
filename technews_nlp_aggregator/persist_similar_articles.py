from technews_nlp_aggregator.jobs import ArticleComparatorJob
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.publish import TfidfFacade
from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from datetime import date
import yaml

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))
db_url    = db_config["db_url"]
articleDatasetRepo = ArticleDatasetRepo(db_url)
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader)
tfidfFacade.load_models()
thresholds = (0.78, 0.995)

for startday in range(1,15):
    print("Executing  {} ".format(str(startday)))
    start = date(2017, 10, startday )
    end = date(2017, 10, startday +1 )

    articleComparatorJob = ArticleComparatorJob(db_url, tfidfFacade, thresholds)
    articleComparatorJob.find_articles(start, end)

