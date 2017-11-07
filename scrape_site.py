from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from technews_nlp_aggregator.scraping.main.scrapy import settings
from technews_nlp_aggregator.scraping.main.scrapy.spiders import ArstechnicaSpider, TechcrunchSpider, ThenextwebSpider, ThevergeSpider, VenturebeatSpider, TechrepublicSpider
from datetime import date, timedelta
from technews_nlp_aggregator import Application
import yaml

def do_crawl(application):
    _ = application
    spiders = ([ThenextwebSpider, ThevergeSpider, VenturebeatSpider, ArstechnicaSpider, TechcrunchSpider, TechrepublicSpider])
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    max_date = _.articleDatasetRepo.get_latest_article_date()
    go_back_date = max_date-timedelta(days=3)
    for spider in spiders:
        process.crawl(spider, _.articleDatasetRepo, max_date)
    process.start()

if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    application = Application(config, True)
    do_crawl(application)


