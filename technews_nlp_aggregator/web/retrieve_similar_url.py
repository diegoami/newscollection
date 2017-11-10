from .util import read_int_from_form
from .merge_tables import retrieve_sims_map, merge_sims_maps,retrieve_sims_map_with_dates
from flask import render_template,  request
from . import app
from datetime import timedelta, date
from technews_nlp_aggregator.common.util import extract_date


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
    _ = app.application
    if request.method == 'POST':
        form = request.form
        if form:

            url = form["tdidf_input"]
            article_id = read_int_from_form(form, 'article_id', 0)
            n_articles = read_int_from_form(form, 'n_articles')
            d_days = read_int_from_form(form, 'd_days')

            if article_id:
                article = _.articleLoader.get_article(article_id)
                url = article.iloc[0]['url']
                id = article.index[0]
            elif url:
                id = _.articleLoader.get_id_from_url(url)

            if (id > _.tfidfFacade.docs_in_model() or id > _.doc2VecFacade.docs_in_model()):
                return retrieve_from_article_id( article_id=article_id, n_articles=n_articles,   url=url, d_days=d_days)
            else:
                return common_retrieve_url( url=url, article_id=article_id, n_articles=n_articles, d_days=d_days)
        else:
            return render_template('search_url.html',
                                       messages=['Please enter the URL of an article or an article id in the databasse'])


def common_retrieve_url(url=None, article_id=None, n_articles=25, d_days=30):
    _ = app.application
    tdf_sims_map = retrieve_articles_url_sims(_.tfidfFacade, url, n_articles, d_days)
    doc2vec_sims_map = retrieve_articles_url_sims(_.doc2VecFacade, url, n_articles, d_days)
    if (not tdf_sims_map or not doc2vec_sims_map ):
        return render_template('search_url.html', messages=['Could not find related URLs in the database'])
    else:
        related_articles = merge_sims_maps(tdf_sims_map, doc2vec_sims_map, _.articleLoader)
        if related_articles:
            return render_template('search_url.html', articles=related_articles[:n_articles], search_url=url, article_id=article_id, n_articles=n_articles,  d_days=d_days)

def retrieve_from_article_id( article_id, n_articles,url,  d_days=30, ):
    _ = app.application
    if article_id is None:
        return render_template('search_url.html', messages=['Could not find the URL in the database'])
    else:
        article = _.articleDatasetRepo.load_article_with_text(article_id)
        title, text, art_date, url = article['AIN_TITLE'], article['ATX_TEXT'], article['AIN_DATE'], article['AIN_URL']
        start, end = art_date-timedelta(d_days), art_date+timedelta(d_days)
        tdf_sims_map = retrieve_sims_map_with_dates(_.tfidfFacade, text=text, start=start, end=end, n_articles=n_articles, title=title)
        doc2vec_sims_map = retrieve_sims_map_with_dates(_.doc2VecFacade, text=text, start=start, end=end, n_articles=n_articles, title=title)
        related_articles = merge_sims_maps(tdf_sims_map, doc2vec_sims_map, _.articleLoader)
        start_s, end_s =  str(start.year)+'-'+str(start.month)+'-'+str(start.day), str(end.year)+'-'+str(end.month)+'-'+str(end.day)
        return render_template('search_url.html', articles=related_articles[:n_articles], search_text=text,
                               n_articles=n_articles, start_s=start_s, end_s=end_s, search_url=url, article_id=article_id)


def retrieve_articles_url_sims(classifier, url, n_articles, d_days):
    articlesIndeces, scores = classifier.get_related_articles_and_score_url(url, d_days)
    if (articlesIndeces is not None):
        max_n_articles = min(len(articlesIndeces), n_articles * 10)
        sims = zip(articlesIndeces[:max_n_articles], scores[:max_n_articles])
        articleMap = {articleIndex: score  for articleIndex, score in sims}

        return articleMap
    else:
        return None