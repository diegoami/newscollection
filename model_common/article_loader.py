import json
import os

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class ArticleLoader:


    def __init__(self, listname, dirname):
        self.listname = listname
        self.dirname  = dirname
        self.article_map = {}

    def load_articles_from_directory(self, load_texts=True):
        with open(self.listname, 'r') as lst_f:
            self.article_map = json.load(lst_f)
            for url in sorted(self.article_map):
                record = self.article_map[url]
                if (load_texts):
                    filename = self.dirname + '/' + record["filename"]
                    if (os.path.isfile(filename)):

                        with open(filename, 'r') as f:
                            text = f.read()
                            record["text"] = text