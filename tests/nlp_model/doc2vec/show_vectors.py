import logging

import yaml
from technews_nlp_aggregator.application import Application

def parse_articles_with_docvec(application, n=100):
    _ = application
    for i in range(n):
        index, article = _.articleLoader.get_random_article()
        article_with_text = _.articleDatasetRepo.load_article_with_text(article['article_id'])
        print(article_with_text)
        vector = _.doc2VecInfo.get_vector_for_docid(index)
        print(vector)


if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    parse_articles_with_docvec(application )
