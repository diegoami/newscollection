# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from technews_nlp_aggregator.persistence import ArticleDatasetRepo

from nltk.tokenize import sent_tokenize
class Pipeline(object):
    def process_item(self, item, spider):
        #text = item['text']
        #sentences = sent_tokenize(text)
        #for sentence in sentences:
        #    print(sentence)
        if (len(item["title"]) >= 10) and (len(item["text"]) >= 600):
            exists = spider.article_repo.update_article(item["url"], item)
            if not exists:
                found = spider.article_repo.save_article( item["url"], item, item["text"])
        return item