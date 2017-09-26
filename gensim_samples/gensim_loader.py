import json


from gensim import corpora, models, similarities

import os

from gensim.corpora import MmCorpus
import logging
from glob import glob
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import glob
import json
class GensimLoader:

    def __init__(self):
        self.articles, self.titles, self.texts, self.urls = [], [], [], []

    def load_articles_from_json(self, article_filename):
        with open(article_filename) as f:
            jsload = json.load(f)
            posts = jsload
            if "posts" in jsload:
                posts = jsload["posts"]
            for post in jsload["posts"]:
                title = post["title"]
                text = post["text"]
                url = post["url"]
                self.articles.append(title + '\n' + text)
                self.titles.append(title)
                self.texts.append(text)
                self.urls.append(url)


    def load_articles_from_directory(self, dirname):
        gsearch_results = glob.glob(dirname+'/*.txt')
        for gsearch_result in gsearch_results:
            with open(gsearch_result, 'r') as f:
                url = f.readline()
                title = f.readline()
                text = "\n".join(f.readlines())
                self.articles.append(title + '\n' + text)
                self.titles.append(title)
                self.texts.append(text)
                self.urls.append(url)
