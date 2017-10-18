

from technews_nlp_aggregator.nlp_model.common import ArticleLoader, Tokenizer, SentenceTokenizer
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
import yaml
from collections import Counter
import operator


config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))
articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articlesDF = articleLoader.load_all_articles(load_text=True)
sentenceTokenizer = SentenceTokenizer()
lastsentences_map = {}
for index, row in articlesDF.iterrows():

    sentences = sentenceTokenizer.process(row['title'], row['text'])
    lastsentence = sentences[-1]
    lgmap = lastsentences_map.get(lastsentence) or 0
    lastsentences_map[lastsentence] = lgmap+1

sorted_x = sorted(lastsentences_map .items(), key=operator.itemgetter(1), reverse=True)
print(sorted_x[:100])