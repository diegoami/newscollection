
from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.append('..')
from gensim_samples.gensim_classifier import GensimClassifier
from gensim_samples.gensim_loader import GensimLoader
from gensim_samples.doc2vec_classifier import Doc2VecClassifier
from os.path import basename
import abc
from urllib.parse import urlparse
import os, glob
app = Flask(__name__)
api = Api(app)
import logging
logging.basicConfig(filename='logs/info.log',level=logging.INFO)
gensim_modelfile = "models/lsi/artmodel_2017-09-29T19:41:07.361378"
gensimLoader = GensimLoader()
gensimLoader.load_articles_from_directory(listname='/home/diego/qdata/techarticles/lists/article_list_29_09_2017b.json',
                                               dirname='/home/diego/qdata/techarticles/parsed_articles/')
gensimClassifier = GensimClassifier(dict_filename=gensim_modelfile + '.dict',
                                         corpus_filename=gensim_modelfile + '.mm', lsi_filename=gensim_modelfile + '.lsi',
                                         index_filename=gensim_modelfile + '.index')

print("Using file {}".format(gensim_modelfile ))

doc2vecClassifier = Doc2VecClassifier(model_filename='models/doc2vec/doc2vecmodel_2017-09-29T20:22:54.683845.model')

doc2vecClassifier.load_models()

gensimClassifier.load_models()

class ClassifierService(Resource):

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
        related_articles = self.retrieve_related_articles(text, n_articles)
        print(related_articles)
        return {

            'related_articles': related_articles
        }

class GensimClassifierService(ClassifierService):


    def retrieve_related_articles(self, doc, n):
        sims = gensimClassifier.get_related_articles(doc, n)
        related_articles = []
        for sim in sims[:n]:
            title = gensimLoader.titles[sim[0]]
            url = gensimLoader.urls[sim[0]]
            tags = gensimLoader.tag_list[sim[0]]
            source = str(urlparse(gensimLoader.urls[sim[0]])[1]).upper()
            tag_base = [x.split('/')[-1] if len(x.split('/')[-1]) > 0 else x.split('/')[-2] for x in
                        gensimLoader.tag_list[sim[0]]]

            similarity = sim[1] * 100

            related_article = {"title": title,
                               "url": url,
                               "tags": tags,
                               "source": source,
                               "tag_base": tag_base,
                               "similarity": similarity}

            related_articles.append(related_article)
        return related_articles

    def post(self):
        return self.common_post()

class Doc2VecClassifierService(ClassifierService):
    def retrieve_related_articles(self, doc, n):
        sims = doc2vecClassifier.get_related_articles(doc, n)
        related_articles = []
        for sim in sims[:n]:
            url = sim[0]
            link_obj = gensimLoader.article_map[url]

            title = link_obj["title"]
            tags = link_obj["tags"]
            source = str(urlparse(url)[1]).upper()
            tag_base = [x.split('/')[-1] if len(x.split('/')[-1]) > 0 else x.split('/')[-2] for x in
                        tags]

            similarity = sim[1] * 100

            related_article = {"title": title,
                               "url": url,
                               "tags": tags,
                               "source": source,
                               "tag_base": tag_base,
                               "similarity": similarity}

            related_articles.append(related_article)
        return related_articles


    def post(self):
        return self.common_post()


#files = glob.glob("models/lsi/artmodel_*.dict")
#files.sort(key=os.path.getmtime)

api.add_resource(GensimClassifierService, '/gensim/')

api.add_resource(Doc2VecClassifierService, '/doc2vec/')



if __name__ == '__main__':
    app.run(debug=True)


