
from flask import  request, render_template, session
from technews_nlp_aggregator.nlp_model.spacy.utils import retrieve_entities

import logging
import traceback



from . import app


#

DEFAULT_FILTER_CRITERIA = 'P_SCORE > 0.6  OR ( U_SCORE > 0.5 )'

@app.route('/filterduplicates', methods=['POST'])
def filterduplicates():
    if request.method == 'POST':
        form = request.form
        if form:
            filterCriteria = form["filterCriteria"]
            session['filterCriteria'] = request.form['filterCriteria']
    return duplicates(0)

@app.route('/duplicates', defaults={'page_id': 0})
@app.route('/duplicates/<int:page_id>')
def duplicates(page_id=0):
    _ = app.application
    filter_criteria = session.get('filterCriteria', DEFAULT_FILTER_CRITERIA )
    messages = []
    try:
        all_articles = _.similarArticlesRepo.list_similar_articles(filter_criteria=filter_criteria )
        start, end = page_id*100, (page_id+1)*100
        if (len(all_articles) > start):
            has_next = len(all_articles) > end
            dup_articles = all_articles[start:min(end,len(all_articles))]
        else:
            dup_articles = []
            return render_template('duplicates.html', messages=['No articles found with this query'],
                                   filter_criteria=filter_criteria)

        return render_template('duplicates.html', dup_articles=dup_articles, page_id=page_id, has_next=has_next, filter_criteria=filter_criteria)
    except:
        traceback.print_exc()
        return render_template('duplicates.html',  filter_criteria=filter_criteria, messages=['Could not execute query - filter criteria are not valid'])
