import logging
from datetime import date

import yaml
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from technews_nlp_aggregator.scraping.main.scrapy import settings
from technews_nlp_aggregator.scraping.main.scrapy.spiders import ArstechnicaSpider, TechcrunchSpider, ThenextwebSpider, ThevergeSpider, VenturebeatSpider, TechrepublicSpider, WiredSpider, EngadgetSpider, GizmodoSpider, MashableSpider, ZdnetSpider, DigitaltrendsSpider, GuardianSpider
from datetime import  timedelta
from technews_nlp_aggregator.persistence import ArticleDatasetRepo, ArticlesSpiderRepo
from technews_nlp_aggregator.scraping.main.scrapy import settings

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
def do_crawl(articleDatasetRepo, spidermap):


    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    for spider_name in spidermap:
        spider = globals()[spider_name+"Spider"]
        urls = spidermap[spider_name]
        process.crawl(spider, articleDatasetRepo, date.min, urls)
    process.start()

if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    db_config = yaml.safe_load(open(config["root_dir"]+config["key_file"]))
    db_url = db_config["db_url"]
    articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"))
    articleSpiderRepo = ArticlesSpiderRepo(db_config.get("db_url"))
    url_queued = articleSpiderRepo.retrieve_urls_queued()
    to_process = {}
    for row in url_queued:
        list_to_process = to_process.get(row["UTA_SPIDER"], [])
        list_to_process.append(row["UTA_URL"])
        to_process[row["UTA_SPIDER"]] = list_to_process


    do_crawl(articleDatasetRepo, to_process)

