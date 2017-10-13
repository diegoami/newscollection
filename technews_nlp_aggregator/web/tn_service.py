
from datetime import date

import yaml
from flask import Flask, request
from flask_restful import Resource, Api

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade
from technews_nlp_aggregator.web.util import extract_related_articles, filter_double, extract_interesting_articles
from technews_nlp_aggregator.common.util import conv_to_date
config = yaml.safe_load(open('config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)

articleLoader.load_all_articles(load_text=False, load_meta=False)
doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader)
doc2VecFacade.load_models()
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader)
tfidfFacade.load_models()
app = Flask(__name__)
api = Api(app)
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from datetime import timedelta

class ClassifierService(Resource):
    def __init__(self):
        self.classifier = None

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response


    def retrieve_articles_srv(self):
        if self.classifier:
            request_body = request.get_json()
            text = request_body["text"]
            n_articles = int(request_body["n_articles"])
            logging.debug(request_body)
            if "start" in request_body and "end" in request_body:
                start, end = conv_to_date(request_body["start"]), conv_to_date(request_body["end"])
                if start and end:
                    sims_all = self.classifier.get_related_articles_from_to(text,  n_articles, conv_to_date(request_body["start"]), conv_to_date(request_body["end"]) )
                else:
                    sims_all = self.classifier.get_related_articles_and_score_doc(text, n_articles)

            else:
                sims_all = self.classifier.get_related_articles_and_score_doc(text, n_articles)
            sims = sims_all[:n_articles]
            logging.info(sims)
            related_articles = extract_related_articles(articleLoader, sims)
            for related_article in related_articles:
                articleLoader.articlesRepo.load_meta(related_article)

            return {
                'related_articles': related_articles
            }
        else:
            return {}

    def retrieve_interesting_articles_srv(self):
        if self.classifier:
            request_body = request.get_json()
            logging.debug(request_body)
            n_articles = int(request_body["n_articles"])
            start_s, end_s = request_body["start"], request_body["end"]
            start, end = conv_to_date(start_s), conv_to_date(end_s)
            if (start == None) or (end == None):
                end = date.today()
                start = end-timedelta(days=5)
            sims_all =  self.classifier.interesting_articles_for_day(start, end, n_articles )
            sims_filtered = filter_double(articleLoader, sims_all )
            interesting_articles = extract_interesting_articles(articleLoader, sims_filtered )
            for interesting_article in interesting_articles :
                articleLoader.articlesRepo.load_meta(interesting_article)

            return {
                'interesting_articles': interesting_articles
            }
        else:
            return {}


class TfidfRetrieveRelatedService(ClassifierService):


    def __init__(self):
        super().__init__()
        self.classifier = tfidfFacade

    def post(self):
        return self.retrieve_articles_srv()

class Doc2VecRetrieveRelatedService(ClassifierService):


    def __init__(self):
        super().__init__()
        self.classifier = doc2VecFacade
#
    def post(self):
        return self.retrieve_articles_srv()

class TfidfRetrieveInterestingService(ClassifierService):


    def __init__(self):
        super().__init__()
        self.classifier = tfidfFacade

    def post(self):
        return self.retrieve_interesting_articles_srv()

class Doc2VecRetrieveInterestingService(ClassifierService):



    def __init__(self):
        super().__init__()
        self.classifier = doc2VecFacade

    def post(self):
        return self.retrieve_interesting_articles_srv()


api.add_resource(TfidfRetrieveRelatedService, '/tfidf/v1/related/')
api.add_resource(Doc2VecRetrieveRelatedService, '/doc2vec/v1/related/')


api.add_resource(TfidfRetrieveInterestingService, '/tfidf/v1/interesting/')
api.add_resource(Doc2VecRetrieveInterestingService, '/doc2vec/v1/interesting/')



if __name__ == '__main__':
    app.run(debug=True, port=80)

