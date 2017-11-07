import yaml

from technews_nlp_aggregator import create_pickle, create_gram_model, create_tfidf_model, create_doc2vec_model, Application
from scrape_site import do_crawl

if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))

    application = Application(config, True)
    do_crawl(application)
    create_pickle(application, config)
    create_gram_model(application)
    create_tfidf_model(application)
    create_doc2vec_model(application)