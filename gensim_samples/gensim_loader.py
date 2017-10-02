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


    def load_articles_from_directory(self, listname, dirname, load_texts=True):
        with open(listname, 'r') as lst_f:
            self.article_map = json.load(lst_f)
            for url in sorted(self.article_map):
                record = self.article_map[url]
                filename = dirname + '/' + record["filename"]
                if (os.path.isfile(filename)):
                    if load_texts:
                        with open(filename, 'r') as f:
                            text = f.read()
                            if (len(text) > 400):
                                self.articles.append(text)
                                self.texts.append(text)
                                self.titles.append(record["title"])
                                self.urls.append(url)



