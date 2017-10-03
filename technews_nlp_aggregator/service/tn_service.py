
from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.append('..')
from datetime import date
import abc
from urllib.parse import urlparse

app = Flask(__name__)
api = Api(app)
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from technews_nlp_aggregator.model_common import ArticleLoader
from technews_nlp_aggregator.model_usage import Doc2VecFacade, TfidfFacade
import yaml

config = yaml.safe_load(open('config.yml'))



articleLoader = ArticleLoader(listname=config["list_name"],dirname=config["parsed_articles_dir"])
articleLoader.load_articles_from_directory(True)
doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader)
doc2VecFacade.load_models()
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader)
tfidfFacade.load_models()

class ClassifierService(Resource):
    def __init__(self):
        self.classifier = None
        self.interest_map = {}

    def extract_source(self, url):
        source = str(urlparse(url)[1]).upper()
        return source

    def extract_date(self, url):
        arrs = str(urlparse(url)[2]).split('/')
        index = 0
        while not arrs[index].isdigit():
            index += 1
        year, month, day = arrs[index], arrs[index+1], arrs[index+2]
        date_str = day + '-' + month + '-' + year

        return date_str

    def extract_tags(self, tags):
        tag_base = [x.split('/')[-1] if len(x.split('/')[-1]) > 0 else x.split('/')[-2] for x in
                    tags]
        return tag_base


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    def retrieve_related_articles(self, doc, n):
        if self.classifier:
            return self.classifier.get_related_articles_and_score_doc(doc, n)
        else:
            return []

    def retrieve_articles_srv(self):
        request_body = request.get_json()
        text = request_body["text"]
        n_articles = request_body["n_articles"]
        logging.debug(request_body)
        related_articles = self.publish_related_articles(text, n_articles)
        print(related_articles)
        return {

            'related_articles': related_articles
        }

    def retrieve_interesting_articles(self, start, end, n):

        if self.classifier:
            logging.info("retrieve_ineresting_article "+str(start) + " "+str(end))
            return self.classifier.interesting_articles_for_day(start, end)
        else:
            return []


    def retrieve_interesting_articles_srv(self):

        def conv_to_date(str_date):
            return date(*(map(int,str_date.split('-'))))

        request_body = request.get_json()
        logging.debug(request_body)
        start_s, end_s = request_body["start"], request_body["end"]
        start, end = conv_to_date(start_s), conv_to_date(end_s)
        if (start, end) in self.interest_map:
            interesting_articles = self.interest_map(start,end)
        else:


            sims_all = self.retrieve_interesting_articles(start, end)
            sims = [(x[0],x[1]) for x in sims_all]
            interesting_articles = self.extract_releated_articles(sims)
            self.interest_map[(start, end) ] = interesting_articles
        return {

            'interesting_articles ': interesting_articles
        }

    def publish_related_articles(self, doc, n):
        sims_all = self.retrieve_related_articles(doc, n)
        logging.info(" ======== SIMS ==============")

        sims = sims_all[:n]
        logging.info(sims)
        related_articles = self.extract_releated_articles(sims)

        return related_articles

    def extract_releated_articles(self, sims):
        related_articles = []
        for url, score in sims:
            related_article = {}
            related_article["url"] = url
            link_obj = articleLoader.article_map[url]
            related_article["title"] = link_obj["title"]
            related_article["tags"] = link_obj["tags"]
            related_article["source"] = self.extract_source(url)
            related_article["tag_base"] = self.extract_tags(related_article["tags"])
            related_article["date"] = self.extract_date(related_article["url"])
            related_article["similarity"] = score * 100
            related_article["authors"] = link_obj["authors"]
            related_article["author_base"] = self.extract_tags(related_article["authors"])
            related_articles.append(related_article)
        logging.info(" ======== RELATED ARTICLES ==============")
        logging.info(related_articles)
        return related_articles


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

#files = glob.glob("models/lsi/artmodel_*.dict")
#files.sort(key=os.path.getmtime)

api.add_resource(TfidfRetrieveRelatedService, '/tfidf/v1/related/')

api.add_resource(Doc2VecRetrieveRelatedService, '/doc2vec/v1/related/')


api.add_resource(TfidfRetrieveInterestingService, '/tfidf/v1/interesting/')

api.add_resource(Doc2VecRetrieveInterestingService, '/doc2vec/v1/interesting/')



if __name__ == '__main__':
    app.run(debug=True)


