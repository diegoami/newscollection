#################
#### imports ####
#################
from flask import Flask
from flask import render_template
from flask import request


from datetime import date

import yaml
from flask import Flask
from technews_nlp_aggregator.persistence.similar_articles import  SimilarArticlesRepo
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo

config = yaml.safe_load(open('config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))
db_url    = db_config["db_url"]
similarArticlesRepo = SimilarArticlesRepo(db_url)

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
app = Flask(__name__)

from random import randint
from . import app
from . import views

@app.route('/')
def index():
    return "Hello World!"


@app.route('/duplicates/<int:page_id>')
def duplicates(page_id=0):
    all_articles = similarArticlesRepo.list_similar_articles()
    start, end = page_id*100, (page_id+1)*100
    if (len(all_articles) > start):
        has_next = len(all_articles) > end
        dup_articles = all_articles[start:min(end,len(all_articles))]
    else:
        dup_articles = []
    return render_template('duplicates.html', dup_articles=dup_articles, page_id=page_id, has_next=has_next)


@app.route('/compare/<int:id1>/<int:id2>')
def compare(id1, id2):
    article1, article2 = articleDatasetRepo.load_articles_with_text(id1, id2)
    return render_template('to_compare.html', A1=article1, A2=article2)

@app.route('/randomrelated')
def randomrelated():
    all_similar_articles = similarArticlesRepo.list_similar_articles()
    len_similar_articles= len(all_similar_articles )
    rlena = randint(0,len_similar_articles)
    similar_article_pair = all_similar_articles[rlena]
    id1, id2 = similar_article_pair["ID_1"], similar_article_pair["ID_2"]
    return compare(id1, id2)

def save_user_association(id1,id2, similarity):
    similarArticlesRepo.persist_user_association(id1, id2, similarity, request.environ['REMOTE_ADDR'])
    return randomrelated()

@app.route('/samestory/<int:id1>/<int:id2>')
def samestory(id1, id2):
    return save_user_association(id1,id2, 0.9)

@app.route('/stronglyrelated/<int:id1>/<int:id2>')
def stronglyrelated(id1, id2):
    return save_user_association(id1, id2, 0.75)

@app.route('/related/<int:id1>/<int:id2>')
def related(id1, id2):
    return save_user_association(id1, id2, 0.5)

@app.route('/unrelated/<int:id1>/<int:id2>')
def unrelated(id1, id2):
    return save_user_association(id1, id2, 0.25)
