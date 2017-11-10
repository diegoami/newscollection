
from flask import render_template,  request
from .summary import get_highlighted_text
from technews_nlp_aggregator.web.summary import convert_summary
from . import app

@app.route('/statistics_random', methods=['POST'])
def statistics_random():
    index, article = app.application.articleLoader.get_random_article()
    article_id = article['article_id']
    return statistics(article_id)


@app.route('/statistics_form', methods=['POST'])
def statistics_form():
    _ = app.application
    if request.method == 'POST':
        form = request.form
        if form:
            article_id = form.get("article_id", None)
            search_url = form.get("search_url", None)
            if (article_id and article_id.isdigit()):
                article_id = int(article_id)
                return statistics(article_id)
            elif (search_url and len(search_url.strip()) > 0):
                article_id = _.articleLoader.get_id_from_url(url=search_url)
                return statistics(article_id)
            else:
                return render_template('statistics.html', messages = ['Please enter a valid article id or an url'])

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
            id = row.index[0]
            if id <= _.tfidfFacade.docs_in_model() or id <= _.doc2VecFacade.docs_in_model():
                tokens = _.tokenizeInfo.get_tokenized_article(title=article["AIN_TITLE"], text=article["ATX_TEXT"])
                trigrams = _.gramFacade.phrase(tokens)
                bows = _.lsiInfo.get_words_docid(id)
                topics = _.lsiInfo.get_topics_docid(id)
                docvecs= _.doc2VecInfo.get_vector_for_docid(id)
                article = convert_summary(article_id)
                return render_template('statistics.html', A=article, tokens=trigrams, bows=bows, topics=topics,
                                       docvecs=docvecs, article_id=article_id, search_url=article["AIN_URL"])
            else:

                saved_text = article['ATX_TEXT']
                bows_vec = _.tfidfFacade.get_doc_bow(title=article['AIN_TITLE'], text=saved_text)
                bows = _.lsiInfo.get_bows_with_id(bows_vec)
                topics = _.tfidfFacade.get_vec(title=article['AIN_TITLE'], text=saved_text)
                tokens = _.tfidfFacade.get_tokenized(title=article['AIN_TITLE'], doc=saved_text)
                docvecs = _.doc2VecFacade.get_vector_for_doc(title=article['AIN_TITLE'], doc=saved_text)
                summaries = _.summaryFacade.summarize_text(title=article['AIN_TITLE'], text=saved_text)
                summary_text = get_highlighted_text(summaries)
                article['ATX_TEXT'] = summary_text
                return render_template('statistics.html', A=article, tokens=tokens, bows=bows, topics=topics,
                                       docvecs=docvecs, article_id=article_id, search_url=article["AIN_URL"])


        else:
            return render_template('statistics.html')
    else:
        return render_template('statistics.html')
