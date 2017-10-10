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
        self.article_map = {}
        self.url_list = []



    def get_random_article(self):
        url_len = len(self.url_list)
        rand_len = randint(1,url_len)-1
        return self.url_list[rand_len]


    def articles_in_interval(self,start, end):
        return [k for k,v in self.article_map.items() if start <= v["date_p"] <= end]

    def docs_in_interval(self, start, end):
        return [i for i,k in enumerate(self.url_list) if start <= self.article_map[k]["date_p"] <= end]


    def load_all_articles(self, load_texts=True):
        self.article_map = OrderedDict()
        self.url_list    = []
        all_articles =  self.articlesRepo.load_articles()
        for article in all_articles:
            url = article["url"]
            self.article_map[url] = article
            self.url_list.append(url)
