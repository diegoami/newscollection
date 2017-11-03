import yaml
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
config = yaml.safe_load(open('../../config.yml'))

db_config = yaml.safe_load(open(config["key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articles = articleDatasetRepo.load_articles()

#for article in articles[:10]:
#    print(article)
print(articles.head())


articles10 = articles[:10]
articles10 = articleDatasetRepo.load_text(articles10,all=False)

print(articles10)

print(articles10.iloc[2,:]['text'])






articles2 = articleDatasetRepo.load_articles()
print(articles2.head())
print(articles2.info())