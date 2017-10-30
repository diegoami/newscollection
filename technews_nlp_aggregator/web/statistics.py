
from flask import render_template,  request
from . import app

@app.route('/statistics_form', methods=['POST'])
def statistics_form():
    if request.method == 'POST':
        form = request.form
        if form:

            article_id = form.get("article_id")
            if form.get('random_id'):
                index, article = app.application.articleLoader.get_random_article()
                article_id = article['article_id']


            return statistics(article_id)
    else:
        return render_template('statistics.html')

@app.route('/statistics_gen')
def statistics_gen():
    return render_template('statistics.html')

@app.route('/statistics/<int:article_id>')
def statistics(article_id):
    if (article_id and article_id.isdigit()):
        article = app.application.articleDatasetRepo.load_article_with_text(article_id)
        if article:

            article["TAGS"], article["AUTHORS"] = app.application.articleDatasetRepo.retrieve_tags_authors(article_id)
            tokens = app.application.tokenizeInfo.get_tokenized_article(article["AIN_TITLE"], article["ATX_TEXT"])
            row = app.application.articleLoader.articlesDF[app.application.articleLoader.articlesDF['article_id'] == int(article_id)]
            id = row.index[0]
            bows = app.application.lsiInfo.get_words_docid(id)
            topics = app.application.lsiInfo.get_topics_docid(id)
            docvecs=app.application.doc2VecInfo.get_vector_for_docid(id)

            return render_template('statistics.html', A=article, tokens=tokens, bows=bows, topics=topics, docvecs=docvecs, article_id=article_id)
        else:
            return render_template('statistics.html')
    else:
        return render_template('statistics.html')
