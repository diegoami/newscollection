import yaml
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
config = yaml.safe_load(open('../../config.yml'))

db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articles = articleDatasetRepo.load_articles(load_meta=False, load_text=False)

for article in articles[:10]:
    print(article)

