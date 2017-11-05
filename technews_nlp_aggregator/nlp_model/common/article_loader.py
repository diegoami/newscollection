
import logging
from random import randint
from . import exclude_articles
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



class ArticleLoader:


    def __init__(self, articlesRepo):
        self.articlesRepo = articlesRepo

    def get_random_article(self):
        url_len = len(self.articlesDF)
        rand_index = randint(0,url_len)
        return rand_index, self.articlesDF.iloc[rand_index]

    def get_article(self, article_id):
        article_row = self.articlesDF[(self.articlesDF['article_id'] == article_id)]
        return article_row.iloc[0]

    def get_id_from_url(self, url):
        article_row = self.articlesDF[(self.articlesDF['url'] == url)]
        if (len(article_row) > 0):
            article_id = article_row.iloc[0]['article_id']
            return article_id
        else:
            return None

    def articles_in_interval(self,start, end):
        return self.articlesDF[(self.articlesDF['date_p'] >= start) & (self.articlesDF['date_p'] <= end) ]

    def load_all_articles(self, load_text=True, limit=None):
        logging.info("Loading articles...")
        self.articlesDF =  self.articlesRepo.load_articles(load_text=load_text)



        self.articlesDF.reset_index(inplace=True)

        return self.articlesDF

