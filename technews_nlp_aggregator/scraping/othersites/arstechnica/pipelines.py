# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from technews_nlp_aggregator.persistence import ArticleDatasetRepo


class ArstechnicaPipeline(object):
    def process_item(self, item, spider):
        #exists = spider.article_repo.update_article(item["url"], item)
        #if not exists:

        found = spider.article_repo.save_article( item["url"], item, item["text"])
        if (found):
            spider.finished = True
        return item
