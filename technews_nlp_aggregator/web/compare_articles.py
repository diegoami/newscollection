import logging

from flask import request, render_template

from technews_nlp_aggregator.web.summary import convert_summary




from . import app


#


@app.route('/examples')
def examples(page_id=0):
    _ = app.application
    yes_articles = _.similarArticlesRepo.list_similar_articles(filter_criteria=" U_SCORE > 0.9 ")
    almost_articles = _.similarArticlesRepo.list_similar_articles(filter_criteria=" U_SCORE > 0.3 AND U_SCORE < 0.7 ")
    return render_template('examples.html', yes_examples=yes_articles[:8], almost_examples=almost_articles[:8] )



@app.route('/compare/<int:article_id1>/<int:article_id2>')
def compare(article_id1, article_id2):
    _ = app.application
    article1, article2 = convert_summary(article_id1), convert_summary(article_id2)

    return render_template('to_compare.html', A1=article1, A2=article2)


@app.route('/randomrelated')
def randomrelated():
    _ = app.application
    id1, id2 = _.similarArticlesRepo.retrieve_random_related()

    return compare(id1, id2)

def save_user_association(id1,id2, similarity):
    _ = app.application
    _.similarArticlesRepo.persist_user_association(id1, id2, similarity, request.environ['REMOTE_ADDR'])
    return randomrelated()

def save_user_association_xhr(id1,id2, similarity):
    _ = app.application
    _.similarArticlesRepo.persist_user_association(id1, id2, similarity, request.environ['REMOTE_ADDR'])
    return str(similarity), {'Content-Type': 'text/html'}

@app.route('/samestory/<int:id1>/<int:id2>')
def samestory(id1, id2):
    return save_user_association(id1,id2, 1.0)

@app.route('/related/<int:id1>/<int:id2>')
def related(id1, id2):
    return save_user_association(id1, id2, 0.5)

@app.route('/unrelated/<int:id1>/<int:id2>')
def unrelated(id1, id2):
    return save_user_association(id1, id2, 0.0)


@app.route('/samestory_xhr/<int:id1>/<int:id2>')
def samestory_xhr(id1, id2):
    return save_user_association_xhr(id1, id2, 1.0)

@app.route('/related_xhr/<int:id1>/<int:id2>')
def related_xhr(id1, id2):
    return save_user_association_xhr(id1, id2, 0.5)

@app.route('/unrelated_xhr/<int:id1>/<int:id2>')
def unrelated_xhr(id1, id2):
    return save_user_association_xhr(id1, id2, 0.0)


