import logging
import sys
import yaml
from technews_nlp_aggregator.scraping.main.scrapy.pipelines import Pipeline
from technews_nlp_aggregator.persistence import ArticleDatasetRepo, ArticlesSpiderRepo
from technews_nlp_aggregator.scraping.main import do_crawl, create_spider_map
from technews_nlp_aggregator.common import load_config

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
    config = load_config(sys.argv)
    db_config = yaml.safe_load(open(config["key_file"]))
    db_url = db_config["db_url"]
    articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"))
    articleSpiderRepo = ArticlesSpiderRepo(db_config.get("db_url"))
    url_queued = articleSpiderRepo.retrieve_urls_queued()
    result = [(row["UTA_SPIDER"], row["UTA_URL"].strip()) for row in url_queued]
    to_process = create_spider_map(result)
    do_crawl(articleDatasetRepo, to_process)
    print(Pipeline.successfully_crawled)