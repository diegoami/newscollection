from flask import render_template, request

from . import app
from .merge_tables import extract_start_end, extract_related_articles
from .util import read_int_from_form


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
            if not text or len(text.strip()) < 3:
                messages.append('Please enter the text of a technical article')
            n_articles = read_int_from_form(form, 'n_articles')
            page_id = read_int_from_form(form, 'page_id', "0")


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
                new_DF = _.classifierAggregator.retrieve_articles_for_text(text=text, start=start, end=end, n_articles=n_articles, title='', page_id=page_id)
                related_articles = extract_related_articles(_.articleLoader, new_DF)

                return render_template('search.html', articles=related_articles[:n_articles],  search_text=text, n_articles=n_articles, start_s=start_s, end_s=end_s, page_id=page_id )
