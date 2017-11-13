
from flask import  request, render_template, session
from technews_nlp_aggregator.common.util import extract_source
from itertools import product

from . import app

@app.route('/filterbrowse', methods=['POST'])
def filterbrowse():
    if request.method == 'POST':
        form = request.form
        if form:
            filterCriteria = form["filterbrowse"]
            session['filterbrowse'] = request.form['filterbrowse']
    return browse(0)



@app.route('/browse', defaults={'page_id': 0})
@app.route('/browse/<int:page_id>')
def browse(page_id=0):
    _ = app.application

    messages = []
    start, end = page_id * 100, (page_id + 1) * 100
    filter_browse = session.get('filterbrowse', '')
    articlesDF =  _.articleLoader.articlesDF.iloc[::-1]
    if (filter_browse):
        articleFilterDF = articlesDF[articlesDF['title'].str.lower().str.contains(filter_browse.lower())]
    else:
        articleFilterDF = articlesDF
    articleFilterDF = articleFilterDF[start:min(end, len(articleFilterDF ))]
    has_next = len(articleFilterDF ) > end
    articleFilterDF['source'] = articleFilterDF['url'].map(extract_source)
    articles = articleFilterDF.to_dict('records')
    return render_template('browse.html', articles=articles , page_id=page_id, has_next=has_next, filter_browse=filter_browse)

