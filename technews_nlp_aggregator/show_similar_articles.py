from technews_nlp_aggregator.jobs import ArticleComparatorJob
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.persistence import SimilarArticlesRepo
import yaml

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))
db_url    = db_config["db_url"]

similarArticlesRepo = SimilarArticlesRepo(db_url)

all_similar_articles = similarArticlesRepo.list_similar_articles()
for article in all_similar_articles:
    print(article)
