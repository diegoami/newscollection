import json
import os
from collections import OrderedDict
import logging
from datetime import date
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from random import randint

class ArticleLoader:


    def __init__(self, listname, dirname):
        self.listname = listname
        self.dirname  = dirname
        self.article_map = {}
        self.url_list = []

    def parse_date(self, record):
        if not record.get("date"):
            record["date_p"] =date(1970,1,1)
        else:
            year, month, day = map(int, record["date"].split('-'))
            article_day = date(year, month, day)
            record["date_p"] = article_day
            return record

    def get_random_article(self):
        url_len = len(self.url_list)
        rand_len = randint(1,url_len)-1
        return self.url_list[rand_len]


    def articles_of_day(self,day):
        return [k for k,v in self.article_map.items() if v["date_p"] == day]



    def articles_in_interval(self,start, end):
        return [k for k,v in self.article_map.items() if start <= v["date_p"] <= end]

    def docs_in_interval(self, start, end):
        return [i for i,k in enumerate(self.url_list) if start <= self.article_map[k]["date_p"] <= end]

    def load_articles_from_directory(self, load_texts=True):
        with open(self.listname, 'r') as lst_f:
            self.article_map = OrderedDict(json.load(lst_f))
            self.url_list    = list(self.article_map.keys())
            for url in self.article_map:
                record = self.article_map[url]
                record = self.parse_date(record)
                record["source"] = url[:url.index(".com")]
                if (load_texts):
                    filename = self.dirname + '/' + record["filename"]
                    if (os.path.isfile(filename)):

                        with open(filename, 'r') as f:
                            text = f.read()
                            record["text"] = text

