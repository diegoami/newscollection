import yaml
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
config = yaml.safe_load(open('../../config.yml'))

articleDatasetRepo = ArticleDatasetRepo(config["db_url"])
articles = articleDatasetRepo.load_articles()
for article in articles[:10]:
    print(article)
