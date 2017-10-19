import yaml
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
config = yaml.safe_load(open('../../config.yml'))

db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
article1, article2 = articleDatasetRepo.load_articles_with_text(6450,24670)
#for article in articles[:10]:
print(article1)
print(article1["AIN_ID"])

print(article2)

