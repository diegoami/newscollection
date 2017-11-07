import yaml

from technews_nlp_aggregator import create_pickle, update_pickle, create_gram_model, create_tfidf_model, create_doc2vec_model, persist_similar_articles
from technews_nlp_aggregator import Application
from scrape_site import do_crawl

if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))

    application = Application(config, True)
    do_crawl(application)
    create_pickle(application, config)
