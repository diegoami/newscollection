
from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.append('..')
from gensim_samples.gensim_classifier import GensimClassifier
from gensim_samples.gensim_loader import GensimLoader
import os, glob
app = Flask(__name__)
api = Api(app)
import logging
logging.basicConfig(filename='logs/info.log',level=logging.INFO)



class GensimClassifierService(Resource):
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    def __init__(self,**kwargs):
        self.filename = kwargs['filename']
        print('Using file :'+self.filename)
        self.gensimLoader = GensimLoader()
        self.gensimLoader.load_articles_from_directory(dirname='/home/diego/qdata/techarticles/parsed_articles/')

        self.gensimClassifier = GensimClassifier(dict_filename=self.filename  + '.dict',
                                            corpus_filename=self.filename  + '.mm', lsi_filename=self.filename  + '.lsi',
                                            index_filename=self.filename + '.index')

        self.gensimClassifier.load_models()

    def post(self):
        request_body = request.get_json()
        text = request_body["text"]
        n_articles = request_body["n_articles"]
        logging.debug(request_body)
        sims = self.gensimClassifier.get_related_articles(text, n_articles  )
        related_articles = [{"title": self.gensimLoader.titles[sim[0]], "url": self.gensimLoader.urls[sim[0]], "similarity": sim[1] * 100} for sim in sims[:n_articles]]

        return {
            'related_articles': related_articles
        }


files = glob.glob("models/lsi/artmodel_*.dict")
files.sort(key=os.path.getmtime)
print("Using file {}".format(files[0]))

api.add_resource(GensimClassifierService, '/',
    resource_class_kwargs={ 'filename': files[0][:-5]})

if __name__ == '__main__':
    app.run(debug=True)


