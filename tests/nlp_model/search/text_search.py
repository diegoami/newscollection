
from technews_nlp_aggregator.application import Application
from datetime import date
import yaml
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    while True:
        st = input('--> ').lower()
        articles = application.classifierAggregator.retrieve_articles_for_text(
            text=st, start=date.min, end=date.max, n_articles=25, title='', page_i=0
        )
        print(articles)
