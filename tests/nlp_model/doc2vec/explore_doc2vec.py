import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade
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
articleLoader.load_all_articles(False)
doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader)
doc2VecFacade.load_models()
model = doc2VecFacade.model
start = date(2017, 10, 10)

end = date(2017, 10, 11)


articles_Found = doc2VecFacade.compare_articles_from_dates(start, end,(.55,.98))
for art_cp, score in articles_Found.items():
    id, other_id = art_cp
    article, otherarticle = articleLoader.articlesDF.loc[id], articleLoader.articlesDF.loc[other_id]
    print(article['date_p'], otherarticle['date_p'], article['title'], otherarticle['title'], score, sep=',')
