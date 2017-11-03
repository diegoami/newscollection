from .util import extract_related_articles, read_int_from_form
from technews_nlp_aggregator.common.util import conv_to_date
from flask import render_template,  request


from datetime import date

from . import app


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search_url')
def search_url():
    return render_template('search_url.html')


@app.route('/retrieve_similar', methods=['POST'])
def retrieve_similar():
    if request.method == 'POST':
        form = request.form
        if form:
            text = form["tdidf_input"]
            if not text or len(text.strip()) == 0:
                return render_template('search.html', messages=['Please enter the text of a technical article'])
            n_articles = read_int_from_form(form, 'n_articles')
            start_s = form["start"]
            end_s = form["end"]

            related_articles_tdf = retrieve_articles(app.application.tfidfFacade, text, n_articles, start_s, end_s)
            related_articles_doc2vec = retrieve_articles(app.application.doc2VecFacade, text, n_articles, start_s, end_s)

            return render_template('search.html', tdf_articles=related_articles_tdf, doc2vec_articles=related_articles_doc2vec, search_text=text )




@app.route('/random_url', methods=['POST'])
def random_url():
    if request.method == 'POST':
        form = request.form
        if form:
            n_articles = read_int_from_form(form, 'n_articles')


            index, article = app.application.articleLoader.get_random_article()
            return common_retrieve_url(url=article["url"], article_id=article["article_id"],  n_articles=n_articles )

@app.route('/retrieve_similar_url', methods=['POST'])
def retrieve_similar_url():
    if request.method == 'POST':
        form = request.form
        if form:

            url = form["tdidf_input"]
            n_articles = read_int_from_form(form, 'n_articles')
            if url:
                article_id = app.application.articleLoader.get_id_from_url(url)
                if (not article_id):
                    return render_template('search_url.html', messages=['Could not find the URL in the database'])
                else:
                    return common_retrieve_url( url=url, article_id=article_id, n_articles=n_articles)
            else:
                return render_template('search_url.html',
                                       messages=['Please enter the URL of an article in the database'])


def common_retrieve_url(url=None, article_id=None, n_articles=50):
    related_articles_tdf = retrieve_articles_url(app.application.tfidfFacade, url)
    related_articles_doc2vec = retrieve_articles_url(app.application.doc2VecFacade, url)
    if related_articles_tdf and related_articles_doc2vec:
        return render_template('search_url.html', tdf_articles=related_articles_tdf,
                               doc2vec_articles=related_articles_doc2vec, search_url=url, article_id=article_id)
    else:
        return render_template('search_url.html', messages=['Could not find related URLs in the database'])


def retrieve_articles(classifier, text, n_articles, start_s, end_s):
    if start_s:
        start = conv_to_date(start_s)
    if end_s:
        end = conv_to_date(end_s)
    if not start:
        start = date.min
    if not end:
        end = date.max

    articlesIndeces, scores = classifier.get_related_articles_and_score_doc(text, start, end)
    sims = zip(articlesIndeces[:n_articles], scores[:n_articles])
    related_articles = extract_related_articles(app.application.articleLoader, sims)

    return related_articles



def retrieve_articles_url(classifier, url, n_articles):
    articlesIndeces, scores = classifier.get_related_articles_and_score_url(url)
    if (articlesIndeces is not None):
        sims = zip(articlesIndeces[:n_articles], scores[:n_articles])
        related_articles = extract_related_articles(app.application.articleLoader, sims)


        return related_articles
    else:
        return None