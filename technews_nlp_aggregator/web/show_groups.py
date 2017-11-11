
from flask import  request, render_template, session
from technews_nlp_aggregator.nlp_model.spacy.utils import retrieve_entities

import logging
import traceback

from . import app


@app.route('/show_groups')
def show_groups(page_id=0):
    _ = app.application

    messages = []
    all_groups_list = _.articleSimilarLoader.retrieve_user_paired()
    groups_list = all_groups_list [::-1]
    article_groups = []
    for group in groups_list:

        articlesDF = _.articleLoader.articlesDF
        articles_in_groupDF = articlesDF[group]
        article_group = []
        for id, row in articles_in_groupDF.iterrows():
            article = {
                "article_id" : row['article_id'],
                "title" : row['title'],
                "date" : row['date'],
                "url" : row['url']
            }
            article_group.append(article)
