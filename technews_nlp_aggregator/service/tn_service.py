
from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.append('..')

import abc
from urllib.parse import urlparse

app = Flask(__name__)
api = Api(app)
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from technews_nlp_aggregator.model_common import ArticleLoader
from technews_nlp_aggregator.model_usage import Doc2VecFacade, TfidfFacade
import yaml

config = yaml.safe_load(open('../config.yml'))


articleLoader = ArticleLoader(listname=config["list_name"],dirname=config["parsed_articles_dir"])
articleLoader.load_articles_from_directory(True)
doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader)
doc2VecFacade.load_models()
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader)
tfidfFacade.load_models()

class ClassifierService(Resource):

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

    @abc.abstractmethod
    def retrieve_related_articles(self, doc, n):
        return []

    def common_post(self):
        request_body = request.get_json()
        text = request_body["text"]
        n_articles = request_body["n_articles"]
        logging.debug(request_body)
        related_articles = self.publish_related_articles(text, n_articles)
        print(related_articles)
        return {

            'related_articles': related_articles
        }

    def publish_related_articles(self, doc, n):
        sims = self.retrieve_related_articles(doc, n)
        logging.info(" ======== SIMS ==============")
        logging.info(sims)

        related_articles = []
        for sim in sims[:n]:
            related_article = {}
            related_article["url"] = url = sim[0]
            link_obj = articleLoader.article_map[url]
            related_article["title"] = link_obj["title"]
            related_article["tags"] = link_obj["tags"]
            related_article["source"] = self.extract_source(url)
            related_article["tag_base"] = self.extract_tags(related_article["tags"])
            related_article["date"] = self.extract_date(related_article["url"])
            related_article["similarity"] = sim[1]*100
            related_article["authors"] = link_obj["authors"]
            related_article["author_base"] =  self.extract_tags(related_article["authors"])
            related_articles.append(related_article)
        logging.info(" ======== RELATED ARTICLES ==============")
        logging.info(related_articles)

        return related_articles


class GensimClassifierService(ClassifierService):


    def retrieve_related_articles(self, doc, n):
        return tfidfFacade.get_related_articles_and_score_doc(doc, n)

    def post(self):
        return self.common_post()

class Doc2VecClassifierService(ClassifierService):

    def retrieve_related_articles(self, doc, n):
        return doc2VecFacade.get_related_articles_and_score_doc(doc, n)


    def post(self):
        return self.common_post()


#files = glob.glob("models/lsi/artmodel_*.dict")
#files.sort(key=os.path.getmtime)

api.add_resource(GensimClassifierService, '/tfidf/v1/related/')

api.add_resource(Doc2VecClassifierService, '/doc2vec/v1/related/')



if __name__ == '__main__':
    app.run(debug=True)


