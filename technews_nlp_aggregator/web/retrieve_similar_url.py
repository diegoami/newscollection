from .util import read_int_from_form
from .merge_tables import retrieve_sims_map, merge_sims_maps
from flask import render_template,  request
from . import app


@app.route('/search_url')
def search_url():
    return render_template('search_url.html')

@app.route('/random_url', methods=['POST'])
def random_url():
    if request.method == 'POST':
        form = request.form
        if form:
            n_articles = read_int_from_form(form, 'n_articles')
            d_days = read_int_from_form(form, 'd_days')

            index, article = app.application.articleLoader.get_random_article()
            return common_retrieve_url(url=article["url"], article_id=article["article_id"],  n_articles=n_articles,  d_days=d_days )

@app.route('/retrieve_similar_url', methods=['POST'])
def retrieve_similar_url():
    if request.method == 'POST':
        form = request.form
        if form:

            url = form["tdidf_input"]
            n_articles = read_int_from_form(form, 'n_articles')
            d_days = read_int_from_form(form, 'd_days')
            if url:
                article_id = app.application.articleLoader.get_id_from_url(url)
                if (not article_id):
                    return render_template('search_url.html', messages=['Could not find the URL in the database'])
                else:
                    return common_retrieve_url( url=url, article_id=article_id, n_articles=n_articles, d_days=d_days)
            else:
                return render_template('search_url.html',
                                       messages=['Please enter the URL of an article in the database'])


def common_retrieve_url(url=None, article_id=None, n_articles=25, d_days=30):
    _ = app.application
    tdf_sims_map = retrieve_articles_url_sims(_.tfidfFacade, url, n_articles, d_days)
    doc2vec_sims_map = retrieve_articles_url_sims(_.doc2VecFacade, url, n_articles, d_days)
    related_articles = merge_sims_maps(tdf_sims_map, doc2vec_sims_map, _.articleLoader)
    if related_articles:
        return render_template('search_url.html', articles=related_articles[:n_articles], search_url=url, article_id=article_id, n_articles=n_articles,  d_days=d_days)
    else:
        return render_template('search_url.html', messages=['Could not find related URLs in the database'])


def retrieve_articles_url_sims(classifier, url, n_articles, d_days):
    articlesIndeces, scores = classifier.get_related_articles_and_score_url(url, d_days)
    if (articlesIndeces is not None):
        max_n_articles = min(len(articlesIndeces), n_articles * 10)
        sims = zip(articlesIndeces[:max_n_articles], scores[:max_n_articles])
        articleMap = {articleIndex: score  for articleIndex, score in sims}

        return articleMap
    else:
        return None