from flask import render_template, request

from . import app
from .merge_tables import extract_start_end, extract_related_articles
from .util import read_int_from_form


@app.route('/exact_search')
def exact_search():

    return render_template('exact_search.html')

@app.route('/retrieve_search', methods=['POST'])
def retrieve_search():
    _ = app.application
    if request.method == 'POST':
        form = request.form
        if form:
            text = form.get("search_text", None)
            messages = []
            if not text or len(text.strip()) < 3:
                messages.append('Please enter search terms')
            n_articles = read_int_from_form(form, 'n_articles')
            page_id = read_int_from_form(form, 'page_id', "0")

            if (len(messages) > 0):
                return render_template('exact_search.html', messages=messages)
            else:

                found_DF = _.articleLoader.articlesRepo.load_articles_containing(text, page_id, n_articles)

                found_articles = found_DF.to_dict(orient='records')
                return render_template('exact_search.html',  articles=found_articles,  search_text=text, n_articles=n_articles, page_id=page_id)
