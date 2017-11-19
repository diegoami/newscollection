import logging

class FeatureFiller:
    def __init__(self, articleLoader, summaryFacade, classifierAggregator, tfidfFacade, doc2VecFacade):
        self.articleLoader = articleLoader
        self.summaryFacade = summaryFacade
        self.classifierAggregator = classifierAggregator
        self.tfidfFacade = tfidfFacade
        self.doc2VecFacade = doc2VecFacade

    def fill_score_map(self, article_id1, article_id2):
        id1, id2 = self.articleLoader.get_id_from_article_id(article_id1), self.articleLoader.get_id_from_article_id(
            article_id2)
        article1, article2 = self.articleLoader.articlesDF.iloc[id1], self.articleLoader.articlesDF.iloc[id2]
        summary1, summary2 = self.summaryFacade.full_text_summarize(id1, article1['text'], article1['title'], 0.85), \
                             self.summaryFacade.full_text_summarize(id2, article2['text'], article2['title'], 0.85)
        summary1b, summary2b = self.summaryFacade.full_text_summarize(id1, article1['text'], article1['title'], 0.7), \
                               self.summaryFacade.full_text_summarize(id2, article2['text'], article2['title'], 0.7)

        score = {}
        score["SCO_AIN_ID_1"], score["SCO_AIN_ID_2"] = article_id1, article_id2
        score["SCO_T_TEXT"], score["SCO_T_TITLE"], score["SCO_T_SUMMARY"], score[
            "SCO_T_SUMMARY_2"] = self.scores_from_classifiers(self.tfidfFacade, article1,
                                                         article2, id1, id2,
                                                         summary1, summary2, summary1b, summary2b)
        score["SCO_D_TEXT"], score["SCO_D_TITLE"], score["SCO_D_SUMMARY"], score[
            "SCO_D_SUMMARY_2"] = self.scores_from_classifiers(self.doc2VecFacade,
                                                         article1, article2,
                                                         id1, id2, summary1,
                                                         summary2, summary1b, summary2b)

        score["SCO_CW_TEXT"], score["SCO_CW_TITLE"], score["SCO_CW_SUMMARY"], score[
            "SCO_CW_SUMMARY_2"] = self.unique_words_diff(self.classifierAggregator,
                                                    article1,
                                                    article2,
                                                    id1, id2,
                                                    summary1,
                                                    summary2,
                                                    summary1b,
                                                    summary2b
                                                    )
        score["SCO_DAYS"] = abs((article2['date_p'] - article1['date_p']).days)
        logging.info(article1['title'])
        logging.info(article2['title'])

        return score

    def scores_from_classifiers(self, classifier, article1, article2, id1, id2, summary1, summary2, summary1b, summary2b):
        score = classifier.get_score_id_id(id1, id2)
        score_tit = classifier.get_score_doc_doc(article1['title'], article2['title'])
        score_sum = classifier.get_score_doc_doc(article1["title"]+ ".\n "+summary1, article2["title"]+ ".\n "+summary2)
        score_sum_b = classifier.get_score_doc_doc(article1["title"]+ ".\n "+summary1b, article2["title"]+ ".\n "+summary2b)
        return score, score_tit, score_sum, score_sum_b


    def unique_words_diff(self, aggregator, article1, article2, id1, id2, summary1, summary2, summary1b, summary2b):
        cw_tot = aggregator.common_miss_words_doc(article1["title"]+ ".\n "+article1["text"], article2["title"]+ ".\n "+article2["text"])
        cw_tit = aggregator.common_miss_words_doc(article1['title'], article2['title'])
        cw_sum1 = aggregator.common_miss_words_doc(article1["title"]+ ".\n "+summary1, article2["title"]+ ".\n "+summary2)
        cw_sum_b = aggregator.common_miss_words_doc(article1["title"]+ ".\n "+summary1b, article2["title"]+ ".\n "+summary2b)
        return cw_tot, cw_tit, cw_sum1, cw_sum_b
