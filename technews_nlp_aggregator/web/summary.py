from technews_nlp_aggregator.web import app


def convert_summary(article_id):
    _ = app.application
    id =  _.articleLoader.articlesDF[_.articleLoader.articlesDF['article_id'] == article_id].index[0]
    article = _.articleDatasetRepo.load_article_with_text( article_id )
    summary_sentences = _.summaryFacade.summarize( id, article["AIN_TITLE"], article["ATX_TEXT"])
    result = ""
    for highlighted, sentence in summary_sentences:
        if highlighted:
            result = result + " <B> " + sentence +"</B>"
        else:
            result =  result + " " + sentence

    article["ATX_TEXT"] = result
    return article