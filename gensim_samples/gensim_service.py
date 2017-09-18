import pickle as cPickle

import numpy as np
import sklearn.externals.joblib
import argparse
from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.append('..')
from gensim_samples.gensim_lib import GensimClassifier

app = Flask(__name__)
api = Api(app)



class GensimClassifierService(Resource):


    def __init__(self,**kwargs):
        self.filename = kwargs['filename']
        self.gensimClassifier = GensimClassifier(article_filename=self.filename , dict_filename=self.filename  + '.dict',
                                            corpus_filename=self.filename  + '.mm', lsi_filename=self.filename  + '.lsi',
                                            index_filename=self.filename + '.index')
        self.gensimClassifier.load_articles()
        self.gensimClassifier.load_models()

    def post(self):
        request_body = request.get_json()
        text = request_body["text"]
        n_articles = request_body["n_articles"]

        related_articles = self.gensimClassifier.get_related_articles(text, n_articles  )

        return {
            'related_articles': related_articles
        }

api.add_resource(GensimClassifierService, '/',
    resource_class_kwargs={ 'filename': 'data/tech_posts_6.json'})

if __name__ == '__main__':
    app.run(debug=True)


