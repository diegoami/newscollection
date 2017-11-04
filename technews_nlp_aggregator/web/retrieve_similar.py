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

            tdf_sims_map = retrieve_sims_map(app.application.tfidfFacade, text, start_s, end_s, n_articles)
            doc2vec_sims_map = retrieve_sims_map(app.application.doc2VecFacade, text, start_s, end_s,  n_articles)
            related_articles = merge_sims_maps(tdf_sims_map, doc2vec_sims_map)
            return render_template('search.html', articles=related_articles[:n_articles],  search_text=text )




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
    tdf_sims_map = retrieve_articles_url_sims(app.application.tfidfFacade, url, n_articles)
    doc2vec_sims_map = retrieve_articles_url_sims(app.application.doc2VecFacade, url, n_articles)
    related_articles = merge_sims_maps(tdf_sims_map, doc2vec_sims_map)
    if related_articles:
        return render_template('search_url.html', articles=related_articles[:n_articles], search_url=url, article_id=article_id)
    else:
        return render_template('search_url.html', messages=['Could not find related URLs in the database'])


def merge_sims_maps(tdf_sims_map, doc2vec_sims_map):
    both_sims_map = {}
    for tdf_key in tdf_sims_map:
        both_sims_map[tdf_key] = tdf_sims_map.get(tdf_key, 0) + doc2vec_sims_map.get(tdf_key, 0)
    for doc2vec_key in doc2vec_sims_map:
        both_sims_map[doc2vec_key] = tdf_sims_map.get(doc2vec_key, 0) + doc2vec_sims_map.get(doc2vec_key, 0)
    sims = sorted(both_sims_map.items(), key=lambda x: x[1], reverse=True)
    related_articles = extract_related_articles(app.application.articleLoader, sims)
    return related_articles


def retrieve_sims_map(classifier, text, start_s, end_s, n_articles):
    if start_s:
        start = conv_to_date(start_s)
    if end_s:
        end = conv_to_date(end_s)
    if not start:
        start = date.min
    if not end:
        end = date.max

    articlesIndeces, scores = classifier.get_related_articles_and_score_doc(text, start, end)
    max_n_articles = min(len(articlesIndeces), n_articles*10)
    sims = zip(articlesIndeces[:max_n_articles], scores[:max_n_articles])
    articleMap = {articleIndex: score for articleIndex, score in sims }


    return articleMap



def retrieve_articles_url_sims(classifier, url, n_articles):
    articlesIndeces, scores, date_differences = classifier.get_related_articles_and_score_url(url)
    if (articlesIndeces is not None):
        max_n_articles = min(len(articlesIndeces), n_articles * 20)
        sims = zip(articlesIndeces[:max_n_articles], scores[:max_n_articles], date_differences[:max_n_articles])
        articleMap = {articleIndex: score  for articleIndex, score, date_dif in sims}

        return articleMap
    else:
        return None