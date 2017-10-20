#################
#### imports ####
#################
from flask import Flask

from random import randint
from .services import articleDatasetRepo, ArticleLoader, similarArticlesRepo, tfidfFacade, doc2VecFacade, articleLoader, app, render_template, request
from .retrieve_similar import *
from .analyze_articles import *

@app.route('/')
def home():
    return render_template('home.html')