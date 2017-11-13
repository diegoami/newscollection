from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from technews_nlp_aggregator.scraping.main.scrapy import settings
from technews_nlp_aggregator.scraping.main.scrapy.spiders import ArstechnicaSpider, TechcrunchSpider, ThenextwebSpider, ThevergeSpider, VenturebeatSpider, TechrepublicSpider, WiredSpider
from datetime import  timedelta
from technews_nlp_aggregator.persistence import ArticleDatasetRepo
import yaml
import logging
from datetime import date
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
def do_crawl(articleDatasetRepo, spiders, urls):


    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    for spider in spiders:
        process.crawl(spider, articleDatasetRepo, date.min, urls)
    process.start()

if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    db_config = yaml.safe_load(open(config["key_file"]))
    db_url = db_config["db_url"]
    articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"))
    do_crawl(articleDatasetRepo, [WiredSpider], ["https://www.wired.com/story/embark-self-driving-truck-deliveries/"])

