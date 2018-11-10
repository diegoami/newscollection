
from flask import render_template

from technews_nlp_aggregator.web.summary import convert_summary
from . import app


@app.route('/refresh_groups')
def refresh_groups():
    _ = app.application
    _.refresh_groups()
    return show_groups()
@app.route('/')
@app.route('/show_groups', defaults={'page_id': 0})
@app.route('/show_groups/<int:page_id>')
def show_groups(page_id=0):
    _ = app.application
    paging_rate = 20
    back_forth = 6
    messages = []
    start, end = page_id * paging_rate, (page_id + 1) * paging_rate
    article_groups = _.article_groups
    groups_list = article_groups[start:min(end, len(article_groups))]

    has_next = len(article_groups) > end
    how_many_pages = min(max((len(article_groups) - end) // paging_rate, 0),back_forth)
    begin_page = max(0, page_id - back_forth)
    return render_template('show_groups.html', article_groups=groups_list , page_id=page_id, has_next=has_next, how_many_pages=how_many_pages, begin_page = begin_page )


@app.route('/show_all/<string:id_list>')
def show_all(id_list):
    _ = app.application
    article_ids = map(int, id_list.split('-'))
    articles = []
    for article_id in article_ids:
        article = app.application.articleDatasetRepo.load_article_with_text(article_id)
        article = convert_summary(article_id)
        articles.append(article)
    return render_template('show_all.html', articles=articles)
