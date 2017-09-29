
from flask import Flask, request
from flask_restful import Resource, Api

import sys
sys.path.append('..')
from gensim_samples.gensim_classifier import GensimClassifier
from gensim_samples.gensim_loader import GensimLoader
from os.path import basename

from urllib.parse import urlparse
import os, glob
app = Flask(__name__)
api = Api(app)
import logging
logging.basicConfig(filename='logs/info.log',level=logging.INFO)
gensim_modelfile = "models/lsi/artmodel_2017-09-29T18:50:06.906818"
gensimLoader = GensimLoader()
gensimLoader.load_articles_from_directory(listname='/home/diego/qdata/techarticles/lists/article_list_29_09_2017b.json',
                                               dirname='/home/diego/qdata/techarticles/parsed_articles/')
gensimClassifier = GensimClassifier(dict_filename=gensim_modelfile + '.dict',
                                         corpus_filename=gensim_modelfile + '.mm', lsi_filename=gensim_modelfile + '.lsi',
                                         index_filename=gensim_modelfile + '.index')

gensimClassifier.load_models()

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



    def post(self):
        request_body = request.get_json()
        text = request_body["text"]
        n_articles = request_body["n_articles"]
        logging.debug(request_body)
        sims = gensimClassifier.get_related_articles(text, n_articles  )
        related_articles = []
        for sim in sims[:n_articles]:

            title = gensimLoader.titles[sim[0]]
            url =  gensimLoader.urls[sim[0]]
            tags = gensimLoader.tag_list[sim[0]]
            source = urlparse(gensimLoader.urls[sim[0]])[1],
            tag_base =  [x.split('//')[-1] for x in gensimLoader.tag_list[sim[0]] ]

            similarity =  sim[1] * 100

            related_article =  {"title": title,
                                 "url": url,
                                 "tags" : tags,
                                 "source" : source,
                                 "tag_base" : tag_base,
                                 "similarity": similarity}

            related_articles.append(related_article)
        return {

            'related_articles': related_articles
        }


#files = glob.glob("models/lsi/artmodel_*.dict")
#files.sort(key=os.path.getmtime)
print("Using file {}".format(gensim_modelfile ))

api.add_resource(GensimClassifierService, '/gensim/',
    resource_class_kwargs={ 'filename': gensim_modelfile })



if __name__ == '__main__':
    app.run(debug=True)


