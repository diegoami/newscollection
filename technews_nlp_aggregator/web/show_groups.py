
from flask import  request, render_template, session
from technews_nlp_aggregator.common.util import extract_source
from itertools import product

from . import app




@app.route('/show_groups', defaults={'page_id': 0})
@app.route('/show_groups/<int:page_id>')
def show_groups(page_id=0):
    _ = app.application

    messages = []
    start, end = page_id * 100, (page_id + 1) * 100

    all_groups_list = _.articleSimilarLoader.retrieve_groups()
    groups_list = all_groups_list [::-1]
    has_next = len(groups_list) > end
    groups_list = groups_list[start:min(end, len(groups_list))]
    article_groups = []
    for group in groups_list:

        articlesDF = _.articleLoader.articlesDF
        lgroup = list(group)
        articles_in_groupDF = articlesDF[articlesDF['article_id'].isin(group)]
        articles = []
        article_ids = articles_in_groupDF['article_id'].tolist()

        for id, row in articles_in_groupDF.iterrows():
            article = {
                "article_id" : row['article_id'],
                "title" : row['title'],
                "date" : row['date_p'],
                "url" : row['url'],
                "source" : extract_source(row['url']),
                "other_ids" : [article_id for article_id in article_ids if article_id != row['article_id'] ]
            }
            articles.append(article)
        article_groups.append(articles)
    return render_template('show_groups.html', article_groups=article_groups, page_id=page_id, has_next=has_next)

