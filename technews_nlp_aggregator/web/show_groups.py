
from flask import  request, render_template, session
from technews_nlp_aggregator.web.summary import convert_summary


from . import app


@app.route('/refresh_groups')
def refresh_groups():
    _ = app.application
    _.retrieve_groups()
    return show_groups()

@app.route('/show_groups', defaults={'page_id': 0})
@app.route('/show_groups/<int:page_id>')
def show_groups(page_id=0):
    _ = app.application

    messages = []
    start, end = page_id * 100, (page_id + 1) * 100

    all_groups_list = _.all_groups_list
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
                "source" : row['source'],
                "other_ids" : [article_id for article_id in article_ids if article_id != row['article_id'] ]
            }
            articles.append(article)
        article_groups.append({"articles" : articles, "article_list" : "-".join([ str(article["article_id"]) for article in articles ] ) } )
        article_groups.sort(key=lambda article_group : article_group["articles"][0]["date"], reverse=True)
    return render_template('show_groups.html', article_groups=article_groups, page_id=page_id, has_next=has_next)


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
