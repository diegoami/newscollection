#################
#### imports ####
#################
from flask import Flask
from flask import render_template


from datetime import date

import yaml
from flask import Flask, request
from flask_restful import Resource, Api

from technews_nlp_aggregator.persistence.similar_articles import  SimilarArticlesRepo

config = yaml.safe_load(open('config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))
db_url    = db_config["db_url"]
similarArticlesRepo = SimilarArticlesRepo(db_url)

app = Flask(__name__)


from . import app
from . import views

@app.route('/')
def index():
    return "Hello World!"


@app.route('/duplicates')
def duplicates():
    dup_articles = similarArticlesRepo.list_similar_articles()
    return render_template('duplicates.html', dup_articles =dup_articles)
