import json
import os
from collections import OrderedDict
import logging
from random import randint
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



class ArticleLoader:


    def __init__(self, articlesRepo):
        self.articlesRepo = articlesRepo



    def get_random_article(self):
        url_len = len(self.url_list)
        rand_len = randint(1,url_len)-1
        return self.url_list[rand_len]


    def articles_in_interval(self,start, end):
        return self.articlesDF[(self.articlesDF['date_p'] >= start) & (self.articlesDF['date_p'] <= end) ]




    def load_all_articles(self, load_text=True, load_meta=True):

        self.articlesDF =  self.articlesRepo.load_articles(load_text=load_text, load_meta=load_meta)
        return self.articlesDF