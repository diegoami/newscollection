
from technews_nlp_aggregator.scraping.google_search_wrapper import Command, create_google_service, Iterator
from technews_nlp_aggregator.scraping.technews_retriever import Raw_Retriever
from technews_nlp_aggregator.scraping.othersites.arstechnica.spiders import TechcrunchSpider

from technews_nlp_aggregator.persistence import ArticleDatasetRepo

import yaml
import scrapy
from scrapy.crawler import CrawlerProcess

config = yaml.safe_load(open('config.yml'))

db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from technews_nlp_aggregator.scraping.othersites.arstechnica import techcrunch_settings

crawler_settings = Settings()
crawler_settings.setmodule(techcrunch_settings)
process = CrawlerProcess(settings=crawler_settings)

process.crawl(TechcrunchSpider, articleDatasetRepo)
process.start()


