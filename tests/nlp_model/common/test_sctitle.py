

from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer,TechArticlesSentenceTokenizer
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
import yaml


config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))
articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articlesDF = articleLoader.load_all_articles(load_text=True, limit=10)
tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer())
tokenized_docs = tokenizer.tokenize_ddf(articlesDF)
for i in range(10):
    print(" ========================== ")
    print(articlesDF['title'][i])
    print(articlesDF['text'][i])
    print(tokenized_docs[i])