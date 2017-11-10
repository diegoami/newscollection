from .util import read_int_from_form

from flask import render_template,  request
from .merge_tables import retrieve_sims_map_with_dates, merge_sims_maps, extract_start_end


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
            text = form.get("search_text", None)
            messages = []
            if not text or len(text.strip()) < 15:
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
                end, start = extract_start_end(start_s, end_s)

                tdf_sims_map = retrieve_sims_map_with_dates(classifier=_.tfidfFacade, text=text, start=start, end=end, n_articles=n_articles)
                doc2vec_sims_map = retrieve_sims_map_with_dates(classifier=_.doc2VecFacade, text=text, start=start, end=end,  n_articles=n_articles)
                related_articles = merge_sims_maps(tdf_sims_map=tdf_sims_map, doc2vec_sims_map=doc2vec_sims_map, articleLoader=_.articleLoader)
                return render_template('search.html', articles=related_articles[:n_articles],  search_text=text, n_articles=n_articles, start_s=start_s, end_s=end_s )
