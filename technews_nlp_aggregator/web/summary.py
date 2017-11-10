from technews_nlp_aggregator.web import app


def convert_summary(article_id):
    _ = app.application
    id =  _.articleLoader.get_article(article_id).index[0]
    article = _.articleDatasetRepo.load_article_with_text( article_id )
    if id <= _.tfidfFacade.docs_in_model():
        summary_sentences = _.summaryFacade.summarize( id, article["AIN_TITLE"], article["ATX_TEXT"])
    else:
        summary_sentences = _.summaryFacade.summarize_text(article["AIN_TITLE"], article["ATX_TEXT"])
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