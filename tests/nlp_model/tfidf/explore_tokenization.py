import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.publish import TokenizeInfo
import yaml

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.generation import TfidfGenerator
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from datetime import datetime
import yaml
from technews_nlp_aggregator.nlp_model.common import TechArticlesSentenceTokenizer, TechArticlesTokenExcluder, NltkWordTokenizer, DefaultTokenizer

config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(False)
tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer(), token_excluder=TechArticlesTokenExcluder(), word_tokenizer=NltkWordTokenizer())

tokenizeInfo = TokenizeInfo(tokenizer)
from random import randint
for i in range(100):
    index, article = articleLoader.get_random_article()
    article_with_text = articleDatasetRepo.load_article_with_text(article['article_id'] )
    print(article_with_text)
    print(tokenizeInfo.get_tokenized_article(article_with_text['AIN_TITLE'], article_with_text['ATX_TEXT']))