#################
#### imports ####
#################
from flask import Flask
from flask import render_template
from flask import request
from random import randint
import yaml
from technews_nlp_aggregator.persistence.similar_articles import  SimilarArticlesRepo
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade
from technews_nlp_aggregator.rest.util import extract_related_articles, filter_double, extract_interesting_articles
from technews_nlp_aggregator.common.util import conv_to_date

from . import views


config = yaml.safe_load(open('config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)

articleLoader.load_all_articles(load_text=True)
doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader)
doc2VecFacade.load_models()
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader)
tfidfFacade.load_models()


import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

config = yaml.safe_load(open('config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))
db_url    = db_config["db_url"]
similarArticlesRepo = SimilarArticlesRepo(db_url)
classifier = tfidfFacade
articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
app = Flask(__name__)



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

@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/retrieve_similar', methods=['POST'])
def retrieve_articles_srv():
    if request.method == 'POST':
        form = request.form
        if form:
            text = form["tdidf_input"]
            n_articles = int(form["n_articles"])

            start_s = form["start"]
            end_s = form["end"]

            if start_s and end_s :
                start, end = conv_to_date(start_s), conv_to_date(end_s)
                if start and end:
                    articlesDF = classifier.get_related_articles_from_to(text, n_articles,
                                                                              start_s, end_s)
                else:
                    articlesDF = classifier.get_related_articles_in_interval(text, n=10000, reference_day=None,
                                                                                  days=30, max=n_articles)
            else:
                articlesDF = classifier.get_related_articles_in_interval(text, n=10000, reference_day=None, days=30,
                                                                              max=n_articles)
            sims = zip(articlesDF.index, articlesDF['score'])
            related_articles = extract_related_articles(articleLoader, sims)
            return render_template('search.html', articles=related_articles )

"""
@app.before_request
def before_request():
    method = request.form.get('_method', '').upper()
    if method:
        request.environ['REQUEST_METHOD'] = method
        ctx = app._request_ctx_stack.top
        ctx.url_adapter.default_method = method
        assert request.method == method
"""