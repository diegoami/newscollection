import yaml
config = yaml.safe_load(open('config.yml'))


from technews_nlp_aggregator.persistence import ArticleJsonRepo, ArticleDatasetRepo

article_json_repo = ArticleJsonRepo(config['link_file'], config['parsed_base_dir'])
article_json_repo.load_articles()
article_dataset_repo = ArticleDatasetRepo(config['db_url'])
count = 0
for url, article_obj in article_json_repo:

    title, text = article_json_repo.load_text_from_file(article_obj['filename'])
    if (title and text):

        article_dataset_repo.save_article(url, article_obj, text)
        count += 1
        #if (count > 10):
         #   break
    article_dataset_repo.flush()