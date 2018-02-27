from datetime import timedelta

from flask import render_template, request

from technews_nlp_aggregator.web.summary import convert_summary
from . import app
from .util import extract_related_articles
from .util import read_int_from_form


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
            url, article_id = article["url"], article["article_id"]
            return common_retrieve_id(id=index,  d_days=d_days, article_id=article["article_id"],  n_articles=n_articles, url=url )



@app.route('/retrieve_similar_url', methods=['POST'])
def retrieve_similar_url():
    _ = app.application
    if request.method == 'POST':
        form = request.form
        if form:
            article = None
            url = form.get("search_url",None)
            article_id = read_int_from_form(form, 'article_id', None)
            n_articles = read_int_from_form(form, 'n_articles')
            page_id = read_int_from_form(form, 'page_id', "0")

            d_days = read_int_from_form(form, 'd_days')

            if article_id:
                article = _.articleLoader.get_article(article_id)


            elif url:
                article_id = _.articleLoader.get_article_id_from_url(url)
                if article_id is not None:
                    article = _.articleLoader.get_article(article_id)

            if (article is not None and len(article) > 0):
                id = article['index']
                url = article['url']

            else:
                return render_template('search_url.html',
                                       messages=[
                                           'Could not find neither url nor id'])
            if (id > _.tfidfFacade.docs_in_model() or id > _.doc2VecFacade.docs_in_model()):
                return retrieve_from_article_id( article_id=article_id, n_articles=n_articles,    d_days=d_days, page_id = page_id)
            else:
                return common_retrieve_id(  id, d_days, n_articles=n_articles, page_id = page_id, url=url, article_id=article_id)
        else:
            return render_template('search_url.html',
                                       messages=['Please enter the URL of an article or an article id in the databasse'])


def common_retrieve_id( id, d_days, n_articles=25,  page_id = 0, url=None, article_id=None):
    _ = app.application
    new_DF = _.classifierAggregator.retrieve_articles_for_id(id=id, d_days=d_days, n_articles=n_articles, page_id=page_id)

    ssus_DF, sscs_DF = _.similarArticlesRepo.retrieve_ssus_for_id(article_id), _.similarArticlesRepo.retrieve_sscs_for_id(article_id, _.version)
    related_articles = extract_related_articles(_.articleLoader, new_DF, ssus_DF, sscs_DF)

    article = convert_summary(article_id)
    if related_articles:
        return render_template('search_url.html', articles=related_articles, search_url=url, article=article, article_id=article_id, n_articles=n_articles,  d_days=d_days, page_id = page_id)

def retrieve_from_article_id( article_id, n_articles, d_days=30, page_id = 0):
    _ = app.application
    if article_id is None:
        return render_template('search_url.html', messages=['Could not find the URL in the database'])
    else:
        article = convert_summary(article_id)

        title, text, art_date, url = article['AIN_TITLE'], article['ATX_TEXT'], article['AIN_DATE'], article['AIN_URL']


        start, end = art_date - timedelta(d_days), art_date + timedelta(d_days)
        new_DF = _.classifierAggregator.retrieve_articles_for_text(text=article['ATX_TEXT'], start=start, end=end, n_articles=n_articles, title=article['AIN_TITLE'], page_id=page_id )
        related_articles = extract_related_articles(_.articleLoader, new_DF)
        start_s, end_s =  str(start.year)+'-'+str(start.month)+'-'+str(start.day), str(end.year)+'-'+str(end.month)+'-'+str(end.day)
        return render_template('search_url.html', articles=related_articles[:n_articles], search_text=text, article=article,
                               n_articles=n_articles, start_s=start_s, end_s=end_s, search_url=url, article_id=article_id, page_id=page_id)



