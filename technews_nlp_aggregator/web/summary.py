from technews_nlp_aggregator.web import app


def convert_summary(article_id):
    _ = app.application
    id =  _.articleLoader.get_article(article_id).index[0]
    article = _.articleDatasetRepo.load_article_with_text( article_id )
    if id <= _.tfidfFacade.docs_in_model():
        summary_sentences = _.summaryFacade.summarize( id, doc=article["ATX_TEXT"], title=article["AIN_TITLE"], )
    else:
        summary_sentences = _.summaryFacade.summarize_text(doc=article["ATX_TEXT"], title=article["AIN_TITLE"] )
    result = get_highlighted_text(summary_sentences)

    article["ATX_TEXT"] = result
    return article


def get_highlighted_text(summary_sentences):
    result = ""
    for highlighted, sentence in summary_sentences:
        if highlighted:
            result = result + " <B> " + sentence + "</B>"
        else:
            result = result + " " + sentence
    return result