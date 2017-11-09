
from flask import render_template,  request

from technews_nlp_aggregator.web.summary import convert_summary
from . import app

@app.route('/statistics_random', methods=['POST'])
def statistics_random():
    index, article = app.application.articleLoader.get_random_article()
    article_id = article['article_id']
    return statistics(article_id)


@app.route('/statistics_form', methods=['POST'])
def statistics_form():
    if request.method == 'POST':
        form = request.form
        if form:
            article_id = form.get("article_id")
            if (article_id and article_id.isdigit()):
                article_id = int(article_id)
                return statistics(article_id)
            else:
                return render_template('statistics.html', messages = ['Please enter an article id or check the random checkbox'])

    else:
        return render_template('statistics.html')

@app.route('/statistics_gen')
def statistics_gen():
    return render_template('statistics.html')

@app.route('/statistics/<int:article_id>')
def statistics(article_id):
    _ = app.application
    if (article_id):
        article = app.application.articleDatasetRepo.load_article_with_text(article_id)

        if article:
           # sp_words = retrieve_sp_words(article["ATX_TEXT"])
            row = _.articleLoader.get_article(article_id)
            tokens = _.tokenizeInfo.get_tokenized_article(article["AIN_TITLE"], article["ATX_TEXT"])
            trigrams = _.gramFacade.phrase(tokens)
            id = row.index[0]
            bows = _.lsiInfo.get_words_docid(id)
            topics = _.lsiInfo.get_topics_docid(id)
            docvecs= _.doc2VecInfo.get_vector_for_docid(id)
            article = convert_summary(article_id)
            return render_template('statistics.html', A=article,  tokens=trigrams , bows=bows, topics=topics, docvecs=docvecs, article_id=article_id)
        else:
            return render_template('statistics.html')
    else:
        return render_template('statistics.html')
