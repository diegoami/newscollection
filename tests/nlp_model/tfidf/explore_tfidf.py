import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade, GramFacade
import yaml


from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.generation import TfidfGenerator
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from datetime import datetime
import yaml

config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(False)
gramFacade = GramFacade(config["phrases_model_dir_link"])
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader, gramFacade=gramFacade)
tfidfFacade.load_models()
tfidfFacade.lsi.show_topics(num_topics=400, num_words=100, log=True)



