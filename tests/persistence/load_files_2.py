import yaml
from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
config = yaml.safe_load(open('../../config.yml'))

articleDatasetRepo = ArticleDatasetRepo(config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles()
first_urls = articleLoader.url_list[:20]
print(first_urls)
for url in first_urls:
    print(articleLoader.article_map[url])




