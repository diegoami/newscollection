from technews_nlp_aggregator.rest.util import extract_related_articles, filter_double, extract_interesting_articles
from technews_nlp_aggregator.common.util import conv_to_date
from .services import *

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
            n_articles = int(form["n_articles"])

            start_s = form["start"]
            end_s = form["end"]

            related_articles_tdf = retrieve_articles(tfidfFacade, text, n_articles, start_s, end_s)
            related_articles_doc2vec = retrieve_articles(doc2VecFacade, text, n_articles, start_s, end_s)

            return render_template('search.html', tdf_articles=related_articles_tdf, doc2vec_articles=related_articles_doc2vec, search_text=text )


@app.route('/retrieve_similar_url', methods=['POST'])
def retrieve_similar_url():
    if request.method == 'POST':
        form = request.form
        if form:
            url = form["tdidf_input"]
            n_articles = int(form["n_articles"])

            related_articles_tdf = retrieve_articles_url(tfidfFacade, url , n_articles)
            related_articles_doc2vec=retrieve_articles_url(doc2VecFacade, url , n_articles)

            return render_template('search_url.html', tdf_articles=related_articles_tdf, doc2vec_articles=related_articles_doc2vec, search_url=url )


def retrieve_articles(classifier, text, n_articles, start_s, end_s):
    if start_s and end_s:
        start, end = conv_to_date(start_s), conv_to_date(end_s)
        if start and end:
            articlesDF = classifier.get_related_articles_from_to(text, n_articles,
                                                                 start, end)
        else:
            articlesDF = classifier.get_related_articles_in_interval(text, n=10000, reference_day=None,
                                                                     days=30, max=n_articles)
    else:
        articlesDF = classifier.get_related_articles_in_interval(text, n=10000, reference_day=None, days=30,
                                                                 max=n_articles)
    sims = zip(articlesDF.index, articlesDF['score'])
    related_articles = extract_related_articles(articleLoader, sims)
    for articleRecord in related_articles:
        articleLoader.articlesRepo.load_meta_record(articleRecord)
    return related_articles



def retrieve_articles_url(classifier, url, n_articles):

    articlesDF = classifier.get_related_articles_and_score_url(url, n=10000, max=n_articles)
    sims = zip(articlesDF.index, articlesDF['score'])
    related_articles = extract_related_articles(articleLoader, sims)
    for articleRecord in related_articles:
        articleLoader.articlesRepo.load_meta_record(articleRecord)

    return related_articles