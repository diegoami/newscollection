import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader, defaultTokenizer
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade,  GramFacade
import yaml


from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.generation import TfidfGenerator
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo

import yaml
from datetime import date

config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)
gramFacade = GramFacade(config["phrases_model_dir_link"])
doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader, gramFacade)
doc2VecFacade.load_models()
print(articleLoader.articlesDF.head())
for i in range(20):
    random_article_id, random_article=  articleLoader.get_random_article()



    print(" ============= ARTICLE ==================")
    print(random_article['text'])
    print(" ============= DOC2VEC ==================")
    sentences_tokenizer = defaultTokenizer.sentence_tokenizer
    for sentence in sentences_tokenizer.process( random_article['text']):
        scores = doc2VecFacade.compare_docs_to_id(random_article['title'], sentence, random_article_id)
        print(sentence)
        print(scores)

