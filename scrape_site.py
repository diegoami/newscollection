from datetime import timedelta
import logging
import yaml
import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from technews_nlp_aggregator.persistence import ArticleDatasetRepo, ScrapeRepo
from technews_nlp_aggregator.scraping.main.scrapy import settings
from technews_nlp_aggregator.scraping.main.scrapy.pipelines import Pipeline
from technews_nlp_aggregator.scraping.main.scrapy.spiders import ArstechnicaSpider, TechcrunchSpider, ThenextwebSpider, \
    ThevergeSpider, VenturebeatSpider, TechrepublicSpider, EngadgetSpider

from technews_nlp_aggregator.common import load_config
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def do_crawl(articleDatasetRepo,go_back=15):

    spiders = ([ThenextwebSpider, ThevergeSpider, VenturebeatSpider, ArstechnicaSpider, TechcrunchSpider, TechrepublicSpider, EngadgetSpider])

    #spiders = ([EngadgetSpider])

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    max_date = articleDatasetRepo.get_latest_article_date()
    go_back_date = max_date-timedelta(days=go_back)
    for spider in spiders:
        process.crawl(spider, articleDatasetRepo, go_back_date)
    process.start()

def do_remove_uninteresting(articleDatasetRepo):
    articleDatasetRepo.delete_unrelevant_texts()

if __name__ == '__main__':
    config = load_config(sys.argv)
    go_back = config["go_back"]
    #if os.environ("DB_URL"):
    #    db_url = os.environ("DB_URL")
    #else:
    db_config = yaml.safe_load(open(config["key_file"]))
    db_url = db_config["db_url"]
    logging.info("DB_URL: {}".format(db_url))
    articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"))
    scrapeRepo = ScrapeRepo(db_config.get("db_url"))
    do_crawl(articleDatasetRepo, go_back)
    scrapeRepo.save_report(Pipeline.successfully_crawled)