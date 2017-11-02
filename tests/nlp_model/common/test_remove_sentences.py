

from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
import yaml
from collections import Counter
import operator


config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))
articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articlesDF = articleLoader.load_all_articles(load_text=True)
sentenceTokenizer = TechArticlesSentenceTokenizer()
lastsentences_map = {}
first_artDF = articlesDF.iloc[:200,:]
for index, row in first_artDF .iterrows():
    cleaned_text = sentenceTokenizer.clean_sentences(row['text'])
    print(cleaned_text)
    print()
