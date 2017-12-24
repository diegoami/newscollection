from datetime import timedelta

import yaml
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from technews_nlp_aggregator.persistence import ArticleDatasetRepo
from technews_nlp_aggregator.scraping.main.scrapy import settings
from technews_nlp_aggregator.scraping.main.scrapy.spiders import ArstechnicaSpider, TechcrunchSpider, ThenextwebSpider, \
    ThevergeSpider, VenturebeatSpider, TechrepublicSpider, EngadgetSpider


def do_crawl(articleDatasetRepo,go_back=15):

    spiders = ([ThenextwebSpider, ThevergeSpider, VenturebeatSpider, ArstechnicaSpider, TechcrunchSpider, TechrepublicSpider, EngadgetSpider])

    #spiders = ([ThenextwebSpider, ThevergeSpider])

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
    config = yaml.safe_load(open('config.yml'))
    go_back = config["go_back"]
    db_config = yaml.safe_load(open(config["root_dir"]+config["key_file"]))
    db_url = db_config["db_url"]
    articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"))
    do_crawl(articleDatasetRepo, go_back)
