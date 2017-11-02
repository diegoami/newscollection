import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer, TechArticlesTokenExcluder, SimpleTokenExcluder, NltkWordTokenizer

from technews_nlp_aggregator.nlp_model.publish import TfidfFacade, Doc2VecFacade
import yaml


from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
import yaml

config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))
tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer(),
                                 token_excluder=TechArticlesTokenExcluder(),
                             word_tokenizer=NltkWordTokenizer())
articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)
import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en')
#while True:
#random_article_id, random_article = articleLoader.get_random_article()
#random_article_id = 15073
#random_article_url = random_article ['url']

random_article = articleLoader.get_article(13262)
# print(random_article)
doc = nlp(random_article ['text'])
for ent in doc.ents:
    print(ent.label_, ent.text)
