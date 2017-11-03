
from flask import render_template,  request
from technews_nlp_aggregator.nlp_model.spacy import retrieve_sp_words, retrieve_entities
from . import app
from .util import highlight_entities

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
    if (article_id):
        article = app.application.articleDatasetRepo.load_article_with_text(article_id)
        if article:

            article["TAGS"], article["AUTHORS"] = app.application.articleDatasetRepo.retrieve_tags_authors(article_id)
            sp_words = retrieve_sp_words(article["ATX_TEXT"])
            tokens = app.application.tokenizeInfo.get_tokenized_article(article["AIN_TITLE"], article["ATX_TEXT"])
            trigrams = app.application.gramFacade.phrase(tokens )
            row = app.application.articleLoader.articlesDF[app.application.articleLoader.articlesDF['article_id'] == int(article_id)]
            id = row.index[0]
            bows = app.application.lsiInfo.get_words_docid(id)
            topics = app.application.lsiInfo.get_topics_docid(id)
            docvecs=app.application.doc2VecInfo.get_vector_for_docid(id)
            article["ORGANIZATIONS"], article["PERSONS"], article["NOUNS"]= retrieve_entities(article["ATX_TEXT"])
            highlight_entities(article, article["ORGANIZATIONS"], article["PERSONS"], article["NOUNS"])

            return render_template('statistics.html', A=article, sp_words=sp_words, tokens=trigrams , bows=bows, topics=topics, docvecs=docvecs, article_id=article_id)
        else:
            return render_template('statistics.html')
    else:
        return render_template('statistics.html')
