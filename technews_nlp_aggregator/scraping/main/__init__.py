import logging
from datetime import date

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.settings import Settings
from technews_nlp_aggregator.scraping.main.scrapy.spiders import *


from technews_nlp_aggregator.scraping.main.scrapy import settings
from technews_nlp_aggregator.scraping.main.scrapy.pipelines import Pipeline

from technews_nlp_aggregator.scraping.main.scrapy import settings
def do_crawl(articleDatasetRepo, spidermap, stop_after_crawl=True):


    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    for spider_name in spidermap:
        spider_class = spider_name+"Spider"
        if spider_class in globals():
            spider = globals()[spider_name+"Spider"]
            urls = spidermap[spider_name]
            process.crawl(spider, articleDatasetRepo, date.min, urls)
        else:
            logging.error("COULD NOT FIND SPIDER {}".format(spider_name))
    process.start(stop_after_crawl=stop_after_crawl)


def create_spider_map(url_queued):
    to_process = {}
    for spider, url in url_queued:
        if spider and url:
            list_to_process = to_process.get(spider, [])
            list_to_process.append(url)
            to_process[spider] = list_to_process
    return to_process

def do_crawl_run(articleDatasetRepo, spidermap):
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    runner = CrawlerRunner(settings=crawler_settings)

    for spider_name in spidermap:
        spider_class = spider_name + "Spider"
        if spider_class in globals():
            spider = globals()[spider_name + "Spider"]
            urls = spidermap[spider_name]
            runner.crawl(spider, articleDatasetRepo, date.min, urls)
        else:
            logging.error("COULD NOT FIND SPIDER {}".format(spider_name))
