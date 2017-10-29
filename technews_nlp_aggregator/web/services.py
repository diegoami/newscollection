import yaml

from technews_nlp_aggregator.persistence.similar_articles import  SimilarArticlesRepo

from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade, LsiInfo, TokenizeInfo, Doc2VecInfo
from flask import Flask
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer, TechArticlesTokenExcluder, SimpleTokenExcluder, NltkWordTokenizer

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

config = yaml.safe_load(open('config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))
db_url    = db_config["db_url"]

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(load_text=False)
similarArticlesRepo = SimilarArticlesRepo(db_url)
tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer(), token_excluder=TechArticlesTokenExcluder(), word_tokenizer=NltkWordTokenizer())
doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], article_loader=articleLoader, tokenizer=tokenizer  )
doc2VecFacade.load_models()

tfidfFacade = TfidfFacade(config["lsi_models_dir_link"], article_loader=articleLoader, tokenizer=tokenizer   )
tfidfFacade.load_models()

lsiInfo = LsiInfo(tfidfFacade.lsi, tfidfFacade.corpus)
tokenizeInfo = TokenizeInfo(tokenizer)
doc2VecInfo = Doc2VecInfo(doc2VecFacade.model)


app = Flask(__name__)

