import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, GramFacade, Doc2VecInfo

from technews_nlp_aggregator.nlp_model.common import defaultTokenizer

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from datetime import datetime
import yaml

config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(False)
gramFacade = GramFacade(config["phrases_model_dir_link"])

doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], article_loader=articleLoader, gramFacade=gramFacade, tokenizer=defaultTokenizer  )
doc2VecFacade.load_models()
doc2VecInfo = Doc2VecInfo(doc2VecFacade.model)
from random import randint
for i in range(100):
    index, article = articleLoader.get_random_article()
    article_with_text = articleDatasetRepo.load_article_with_text(article['article_id'])
    print(article_with_text)
    vector = doc2VecInfo.get_vector_for_docid(index)
    print(vector)
