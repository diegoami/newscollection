from flask import render_template, request

from . import app
from .merge_tables import extract_start_end, extract_related_articles
from .util import read_int_from_form

@app.route('/exact_search')
def exact_search():

    return render_template('exact_search.html', end_s=app.application.latest_article_date)

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

            start_s = form["start"]
            end_s = form["end"]

            if not start_s or len(start_s.strip()) == 0:
                messages.append('Please enter a start date')

            if not end_s or len(end_s.strip()) == 0:
                messages.append('Please enter an end date')

            if (len(messages) > 0):
                return render_template('exact_search.html', messages=messages)
            else:
                end, start = extract_start_end(start_s, end_s)
                found_DF = _.articleLoader.articlesRepo.load_articles_containing(text_to_search=text, page_id=page_id, n_articles=n_articles, start_s = start_s, end_s = end_s)
                if (len(found_DF) == 0):
                    messages.append('No results found')


                found_articles = found_DF.to_dict(orient='records')
                return render_template('exact_search.html',  articles=found_articles,  search_text=text, n_articles=n_articles, page_id=page_id, start_s=start_s, end_s=end_s, messages=messages)
