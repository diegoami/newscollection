from flask import  request, render_template, session

from itertools import product

from . import app

@app.route('/train_data', defaults={'page_id': 0})
@app.route('/train_data/<int:page_id>')
def train_data(page_id=0):
    _ = app.application
    articlesDF = _.articleLoader.articlesDF[['article_id', 'title', 'date_p', 'url']]

    messages = []
    start, end = page_id * 100, (page_id + 1) * 100
    _.articleSimilarLoader.load_train_data_aug()
    train_dataDF = _.articleSimilarLoader.train_data

    has_next = len(train_dataDF ) > end
    train_dataDF= train_dataDF[start:min(end, len(train_dataDF ))]
    train_with_titlesDF = train_dataDF.merge(articlesDF, left_on='SCO_AIN_ID_1', right_on='article_id', suffixes=('','_1') ).merge(articlesDF, left_on='SCO_AIN_ID_2', right_on='article_id',suffixes=('','_2') )
    train_data = train_with_titlesDF.to_dict('records')
    return render_template('train_data.html', train_data =train_data , page_id=page_id)