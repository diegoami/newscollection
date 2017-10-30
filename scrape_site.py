
from technews_nlp_aggregator.scraping.google_search_wrapper import Command, create_google_service, Iterator
from technews_nlp_aggregator.scraping.technews_retriever import Raw_Retriever
from technews_nlp_aggregator.scraping.othersites.arstechnica.spiders import ArstechnicaSpider, TechcrunchSpider, ThenextwebSpider, ThevergeSpider
from technews_nlp_aggregator.scraping.othersites.arstechnica import ArstechnicaPipeline
from technews_nlp_aggregator.persistence import ArticleDatasetRepo

import yaml
import scrapy
from scrapy.crawler import CrawlerProcess

config = yaml.safe_load(open('config.yml'))

db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"))
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from technews_nlp_aggregator.scraping.othersites.arstechnica import arstechnica_settings, thenextweb_settings, techcrunch_settings, theverge_settings

def do_crawl(settings, spider):
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(spider, articleDatasetRepo)
    process.start()

#do_crawl(arstechnica_settings, ArstechnicaSpider)
#do_crawl(techcrunch_settings,  TechcrunchSpider)
#do_crawl(thenextweb_settings,  ThenextwebSpider)
do_crawl(theverge_settings,  ThevergeSpider)