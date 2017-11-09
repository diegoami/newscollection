from .util import read_int_from_form

from flask import render_template,  request
from .merge_tables import retrieve_sims_map, merge_sims_maps


from . import app


@app.route('/search')
def search():

    return render_template('search.html', end_s=app.application.latest_article_date)

@app.route('/retrieve_similar', methods=['POST'])
def retrieve_similar():
    _ = app.application
    if request.method == 'POST':
        form = request.form
        if form:
            text = form["tdidf_input"]
            messages = []
            if not text or len(text.strip()) == 0:
                messages.append('Please enter the text of a technical article')
            n_articles = read_int_from_form(form, 'n_articles')
            start_s = form["start"]
            end_s = form["end"]

            if not start_s or len(start_s.strip()) == 0:
                messages.append('Please enter a start date')

            if not end_s or len(end_s .strip()) == 0:
                messages.append('Please enter an end date')

            if (len(messages) > 0):
                return render_template('search.html', messages=messages)
            else:
                tdf_sims_map = retrieve_sims_map(_.tfidfFacade, text, start_s, end_s, n_articles)
                doc2vec_sims_map = retrieve_sims_map(_.doc2VecFacade, text, start_s, end_s,  n_articles)
                related_articles = merge_sims_maps(tdf_sims_map, doc2vec_sims_map,_.articleLoader)
                return render_template('search.html', articles=related_articles[:n_articles],  search_text=text, n_articles=n_articles, start_s=start_s, end_s=end_s )


def retrieve_articles_url_sims(classifier, url, n_articles, d_days):
    articlesIndeces, scores = classifier.get_related_articles_and_score_url(url, d_days)
    if (articlesIndeces is not None):
        max_n_articles = min(len(articlesIndeces), n_articles * 10)
        sims = zip(articlesIndeces[:max_n_articles], scores[:max_n_articles])
        articleMap = {articleIndex: score  for articleIndex, score in sims}

        return articleMap
    else:
        return None