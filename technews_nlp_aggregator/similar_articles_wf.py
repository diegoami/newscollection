import sys
sys.path.append('..')
import yaml
from technews_nlp_aggregator.jobs import ArticleComparatorJob
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.common.util import daterange
from datetime import datetime

from .application import Application

def persist_similar_articles(application, start, end):

    def find_with_model(model, thresholds, begin, finish, days_diff):
        for start, end in daterange(begin, finish, days_diff):
            print(start.date(), end.date())
            articleComparatorJob = ArticleComparatorJob(db_url, model, thresholds)
            articleComparatorJob.find_articles(start.date(), end.date())

    _ = application

    db_config = yaml.safe_load(open(config["key_file"]))
    db_url = db_config["db_url"]



    find_with_model(model = _.tfidfFacade, thresholds = (0.64, 0.995),
                    begin = datetime(year=2017, month=1, day=1), finish = datetime(year=2017, month=11, day=3), days_diff=2)

    find_with_model(model = _.doc2VecFacade, thresholds = (0.27, 0.99),
                    begin = datetime(year=2017, month=1, day=1), finish = datetime(year=2017, month=11, day=3), days_diff=2)




if __name__ == '__main__':
    import sys
    sys.path.append('..')
    config = yaml.safe_load(open('../config.yml'))
    application = Application(config, True)
    max_artdate = application.articleDatasetRepo.get_latest_article_date()

    persist_similar_articles(application, start= datetime(year=2017, month=1, day=1), end= datetime(year=2017, month=11, day=3))
