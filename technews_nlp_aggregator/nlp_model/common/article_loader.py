
import logging
from random import randint

from technews_nlp_aggregator.common.util import extract_source_without_www, extract_normpath


class ArticleLoader:


    def __init__(self, articlesRepo):
        self.articlesRepo = articlesRepo

    def get_random_article(self):
        url_len = len(self.articlesDF)
        rand_index = randint(0,url_len)
        return rand_index, self.articlesDF.iloc[rand_index]

    def get_article(self, article_id):
        article_row = self.articlesDF[(self.articlesDF['article_id'] == article_id)].iloc[0]
        return article_row

    def get_id_from_article_id(self, article_id):
        article_row = self.articlesDF[(self.articlesDF['article_id'] == article_id)]
        return article_row.index[0]

    def get_article_id_from_url(self, url):
        url = extract_normpath(url)
        article_row = self.articlesDF[(self.articlesDF['url'] == url)]
        if (len(article_row) > 0):
            article_id = article_row.iloc[0]['article_id']
            return article_id
        else:
            return None

    def are_same_source(self, article_id1, article_id2):
        article1, article2 = self.get_article(article_id1), self.get_article(article_id2)
        same_source =  article1['source'] == article2['source']
        return same_source

    def articles_in_interval(self,start, end):
        return self.articlesDF[(self.articlesDF['date_p'] >= start) & (self.articlesDF['date_p'] <= end) ]

    def load_all_articles(self, load_text=True, load_only_unsaved=False):
        logging.info("Loading articles...")
        self.articlesDF =  self.articlesRepo.load_articles(load_text=load_text, load_only_unsaved=load_only_unsaved)
        self.articlesDF.reset_index(inplace=True)
        self.articlesDF['source'] = self.articlesDF['url'].map(extract_source_without_www)
    
        return self.articlesDF

