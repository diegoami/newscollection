import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade, LsiInfo,  Doc2VecInfo
import yaml
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer, TechArticlesTokenExcluder, SimpleTokenExcluder, NltkWordTokenizer

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.generation import TfidfGenerator
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from datetime import datetime
import yaml

config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(False)
tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer(), token_excluder=TechArticlesTokenExcluder(), word_tokenizer=NltkWordTokenizer())
doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], article_loader=articleLoader, tokenizer=tokenizer  )
doc2VecFacade.load_models()
doc2VecInfo = Doc2VecInfo(doc2VecFacade.model)
from random import randint
for i in range(100):
    index, article = articleLoader.get_random_article()
    article_with_text = articleDatasetRepo.load_article_with_text(article['article_id'])
    print(article_with_text)
    vector = doc2VecInfo.get_vector_for_docid(index)
    print(vector)
