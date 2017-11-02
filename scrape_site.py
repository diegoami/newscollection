
from technews_nlp_aggregator.scraping.google_search_wrapper import Command, create_google_service, Iterator
from technews_nlp_aggregator.scraping.technews_retriever import Raw_Retriever
from technews_nlp_aggregator.scraping.othersites.arstechnica.spiders import ArstechnicaSpider, TechcrunchSpider, ThenextwebSpider, ThevergeSpider, VenturebeatSpider, TechrepublicSpider

from technews_nlp_aggregator.persistence import ArticleDatasetRepo

import yaml
import scrapy
from scrapy.crawler import CrawlerProcess

config = yaml.safe_load(open('config.yml'))

db_config = yaml.safe_load(open(config["key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"))
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from technews_nlp_aggregator.scraping.othersites.arstechnica import settings

def do_crawl(settings, spiders):
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    for spider in spiders:
        process.crawl(spider, articleDatasetRepo)
    process.start()


do_crawl(settings,  [ThenextwebSpider, ThevergeSpider, VenturebeatSpider, ArstechnicaSpider, TechcrunchSpider, TechrepublicSpider])

