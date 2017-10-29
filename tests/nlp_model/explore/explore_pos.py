
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade
import yaml


from technews_nlp_aggregator.nlp_model.common import ArticleLoader

from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo

import yaml
import nltk

from nltk.tokenize import sent_tokenize, word_tokenize



config = yaml.safe_load(open('../../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)
titles = articleLoader.articlesDF['title'].tolist()
texts = articleLoader.articlesDF['text'].tolist()

titles_tokenized = [[word for word in word_tokenize(title .lower())]
         for title in titles]


texts_tokenized = [[word for word in word_tokenize(text.lower())]
         for text in texts]

sents_tokenized = [[sentence for sentence in sent_tokenize(text.lower())]
         for text in texts]
for title_tokenized in titles_tokenized[:100]:
    print(title_tokenized)
    print(nltk.pos_tag(title_tokenized))

for text_tokenized in texts_tokenized[:100]:
    print(text_tokenized)
    print(nltk.pos_tag(text_tokenized))

for sent_tokenized in sents_tokenized [:100]:
    print(sent_tokenized )
