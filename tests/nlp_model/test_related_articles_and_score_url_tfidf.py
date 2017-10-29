import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from technews_nlp_aggregator.nlp_model.publish import TfidfFacade
import yaml


from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
import yaml

config = yaml.safe_load(open('../../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(False)
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader)
tfidfFacade.load_models()



url1 = "https://www.theverge.com/2017/10/22/16518298/google-investigating-pixel-2-xl-screen-burn-in"
url2 = "https://thenextweb.com/contributors/2017/10/22/na-zdorovie-doing-business-with-russians-explained/"

from datetime import date
from itertools import islice

def show_related_articles(facade, article):
    #related_articles_doc2vec = facade.get_related_articles(article, 10000)
    start = date(2017, 3, 1)
    end = date(2017, 10, 28)
    articles_indices, scores = facade.get_related_articles_and_score_url(article)


    print(" ==== related_articles  ==== ")
    for article_idx, score in islice(zip(articles_indices, scores),100):
        print(articleLoader.articlesDF.iloc[article_idx]['title'], score)


#show_related_articles(doc2VecFacade, article1)
#show_related_articles(doc2VecFacade, article2)


show_related_articles(tfidfFacade, url1)
show_related_articles(tfidfFacade, url2)

