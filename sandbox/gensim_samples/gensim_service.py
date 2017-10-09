
import sys

from flask import Flask, request
from flask_restful import Resource, Api

sys.path.append('..')
from sandbox.gensim_samples import GensimClassifier
from sandbox.gensim_samples import GensimLoader
from sandbox.gensim_samples import Doc2VecClassifier
import abc
from urllib.parse import urlparse

app = Flask(__name__)
api = Api(app)
import logging
logging.basicConfig(filename='logs/info.log',level=logging.INFO)
gensim_modelfile = "models/lsi/artmodel_2017-09-30T01:27:54.236406"
gensimLoader = GensimLoader()
gensimLoader.load_articles_from_directory(listname='/home/diego/qdata/techarticles/lists/article_list_30_09_2017.json',
                                               dirname='/home/diego/qdata/techarticles/parsed_articles/')
gensimClassifier = GensimClassifier(dict_filename=gensim_modelfile + '.dict',
                                         corpus_filename=gensim_modelfile + '.mm', lsi_filename=gensim_modelfile + '.lsi',
                                         index_filename=gensim_modelfile + '.index')

print("Using file {}".format(gensim_modelfile ))

doc2vecClassifier = Doc2VecClassifier(model_filename='models/doc2vec/doc2vecmodel_2017-09-30T01:29:19.344507.model')

doc2vecClassifier.load_models()

gensimClassifier.load_models()

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
        related_articles = self.retrieve_related_articles(text, n_articles)
        print(related_articles)
        return {

            'related_articles': related_articles
        }

class GensimClassifierService(ClassifierService):


    def retrieve_related_articles(self, doc, n):
        sims = gensimClassifier.get_related_articles(doc, n)
        return self.aggregate_related_articles(n, sims)

    def aggregate_related_articles(self, n, sims):
        related_articles = []
        for sim in sims[:n]:
            related_article = {}
            related_article["url"] = url = gensimLoader.urls[sim[0]]
            link_obj = gensimLoader.article_map[url]
            related_article["title"] = link_obj["title"]
            related_article["tags"] = link_obj["tags"]
            related_article["source"] = self.extract_source(url)
            related_article["tag_base"] = self.extract_tags(related_article["tags"])
            related_article["date"] = self.extract_date(related_article["url"])
            related_article["similarity"] = sim[1] * 100
            related_article["authors"] = link_obj["authors"]
            related_article["author_base"] = self.extract_tags(related_article["authors"])
            related_articles.append(related_article)
        return related_articles

    def post(self):
        return self.common_post()

class Doc2VecClassifierService(ClassifierService):
    def retrieve_related_articles(self, doc, n):
        sims = doc2vecClassifier.get_related_articles(doc, n)
        related_articles = []
        for sim in sims[:n]:
            related_article = {}
            related_article["url"] = url = sim[0]
            link_obj = gensimLoader.article_map[url]
            related_article["title"] = link_obj["title"]
            related_article["tags"] = link_obj["tags"]
            related_article["source"] = self.extract_source(url)
            related_article["tag_base"] = self.extract_tags(related_article["tags"])
            related_article["date"] = self.extract_date(related_article["url"])
            related_article["similarity"] = sim[1] * 100
            related_article["authors"] = link_obj["authors"]
            related_article["author_base"] =  self.extract_tags(related_article["authors"])
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


