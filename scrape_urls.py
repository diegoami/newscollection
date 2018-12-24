import logging
from datetime import timedelta
import sys
import yaml
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from technews_nlp_aggregator.scraping.main.scrapy.spiders import *


from technews_nlp_aggregator.scraping.main.scrapy import settings
from technews_nlp_aggregator.scraping.main.scrapy.pipelines import Pipeline
from technews_nlp_aggregator.persistence import ArticleDatasetRepo, ArticlesSpiderRepo
from technews_nlp_aggregator.scraping.main.scrapy import settings
from technews_nlp_aggregator.common import load_config

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
def do_crawl(articleDatasetRepo, spidermap, go_back):


    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    for spider_name in spidermap:
        spider_class = spider_name+"Spider"
        if spider_class in globals():
            spider = globals()[spider_name+"Spider"]
            urls = spidermap[spider_name]
            max_date = articleDatasetRepo.get_latest_article_date()
            go_back_date = max_date - timedelta(days=go_back)

            process.crawl(spider, articleDatasetRepo, go_back_date, urls)
        else:
            logging.error("COULD NOT FIND SPIDER {}".format(spider_name))
    process.start()


def create_spider_map(url_queued):
    to_process = {}
    for spider, url in url_queued:
        if spider and url:
            list_to_process = to_process.get(spider, [])
            list_to_process.append(url)
            to_process[spider] = list_to_process
    return to_process

if __name__ == '__main__':
    config = load_config(sys.argv)
    go_back = config["go_back"]
    db_config = yaml.safe_load(open(config["key_file"]))
    db_url = db_config["db_url"]
    logging.info("DB_URL: {}".format(db_url))
    articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"))
    articleSpiderRepo = ArticlesSpiderRepo(db_config.get("db_url"))
    url_queued = articleSpiderRepo.retrieve_urls_queued()
    result = [(row["UTA_SPIDER"], row["UTA_URL"].strip()) for row in url_queued]
    to_process = create_spider_map(result)

    do_crawl(articleDatasetRepo, to_process, go_back)

    print(Pipeline.successfully_crawled)