import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.publish import TokenizeInfo


from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.spacy import spacy_nlp

from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo

import yaml
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer

config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(False)


tokenizeInfo = TokenizeInfo(defaultTokenizer)
from random import randint
for i in range(100):
    index, article = articleLoader.get_random_article()
    article_id = article['article_id']
    article_with_text = articleDatasetRepo.load_article_with_text(article_id  )
    doc = spacy_nlp(article_with_text['ATX_TEXT'])
    lemmas = [(word.text, word.lemma_) for word in doc]

    print(lemmas)