
from flask import  request, render_template, session
from technews_nlp_aggregator.nlp_model.spacy.utils import retrieve_entities

import logging
import traceback

from . import app


@app.route('/show_groups')
def duplicates(page_id=0):
    _ = app.application

    messages = []
    try:
        all_groups = _.articleSimilarLoader.retrieve_user_paired()
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