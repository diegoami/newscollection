import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import yaml


from itertools import islice
from technews_nlp_aggregator.application import Application

def show_related_articles_random_urls(application, n_articles=20):
    _ = application

    def show_related_articles(_, facade, url, d_days = 90):

        articles_indices, scores = facade.get_related_articles_and_score_url(url, d_days )


        print(" ==== related_articles  ==== ")
        for article_idx, score in islice(zip(articles_indices, scores), 25):
            print(_.articleLoader.articlesDF.iloc[article_idx]['title'], score)


    for i in range(n_articles):
        index, article = _.articleLoader.get_random_article()
        show_related_articles(_, _.doc2VecFacade, article['url'] )
        show_related_articles(_, _.tfidfFacade, article['url'])

def show_related_articles_random_docs(application, n_articles=20):
    _ = application

    def show_related_articles(_, facade, text, d_days = 90):

        articles_indices, scores = facade.get_related_articles_and_score_doc(text, d_days )


        print(" ==== related_articles  ==== ")
        for article_idx, score in islice(zip(articles_indices, scores), 25):
            print(_.articleLoader.articlesDF.iloc[article_idx]['title'], score)


    for i in range(n_articles):
        index, article = _.articleLoader.get_random_article()
        show_related_articles(_, _.doc2VecFacade, article['text'] )
        show_related_articles(_, _.tfidfFacade, article['text'])

if __name__ == '__main__':
    config = yaml.safe_load(open('../../config.yml'))
    application = Application(config, True)
    show_related_articles_random_docs(application)
    show_related_articles_random_urls(application)
