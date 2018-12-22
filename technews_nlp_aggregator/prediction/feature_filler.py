import logging
import numpy as np
from .article_features import ArticleFeatures

class FeatureFiller:


    def __init__(self, articleLoader, summaryFacade, classifierAggregator, tfidfFacade, doc2VecFacade, tf2wv_mapper, version):
        self.articleLoader = articleLoader
        self.summaryFacade = summaryFacade
        self.classifierAggregator = classifierAggregator
        self.tfidfFacade = tfidfFacade
        self.doc2VecFacade = doc2VecFacade
        self.tf2wv_mapper = tf2wv_mapper
        self.version = version
        self.features_cache = {}


    def retrieve_features(self, id, article_id, article):
        if id in self.features_cache :
            return self.features_cache [id]
        else:
            self.features_cache[id] = ArticleFeatures(id, article_id, article)
            self.features_cache[id].retrieve_summaries(self.summaryFacade)
            self.features_cache[id].retrieve_tokens(self.tfidfFacade)

            return self.features_cache[id]

    def calc_work_days(self, article_id1, article_id2):
        id1, id2 = self.articleLoader.get_id_from_article_id(article_id1), self.articleLoader.get_id_from_article_id(
            article_id2)
        article1, article2 = self.articleLoader.articlesDF.iloc[id1], self.articleLoader.articlesDF.iloc[id2]
        return abs(np.busday_count(article1['date_p'], article2['date_p']))

    def fill_score_map(self, article_id1, article_id2):
        id1, id2 = self.articleLoader.get_id_from_article_id(article_id1), self.articleLoader.get_id_from_article_id(
            article_id2)
        article1, article2 = self.articleLoader.articlesDF.iloc[id1], self.articleLoader.articlesDF.iloc[id2]
        features_id1, features_id2 = self.retrieve_features(id1, article_id1, article1), self.retrieve_features(id2, article_id2, article2)

        score = {}
        score["SCO_AIN_ID_1"], score["SCO_AIN_ID_2"] = article_id1, article_id2
        score["SCO_T_TEXT"], score["SCO_T_TITLE"], score["SCO_T_SUMMARY"], score[
            "SCO_T_SUMMARY_2"] = self.scores_from_classifiers(self.tfidfFacade, features_id1, features_id2)
        score["SCO_D_TEXT"], score["SCO_D_TITLE"], score["SCO_D_SUMMARY"], score[
            "SCO_D_SUMMARY_2"] = self.scores_from_classifiers(self.tf2wv_mapper, features_id1, features_id2)

        score["SCO_CW_TEXT"], score["SCO_CW_TITLE"], score["SCO_CW_SUMMARY"], score[
            "SCO_CW_SUMMARY_2"] = self.unique_words_diff(self.classifierAggregator, features_id1, features_id2)
        score["SCO_DAYS"] = abs((article2['date_p'] - article1['date_p']).days)
        score["SCO_W_DAYS"] = np.busday_count(article1['date_p'], article2['date_p'])
        score["SCO_VERSION"] = self.version
        logging.info("TITLE : {} , DATE : {} ".format(article1['title'],article1['date_p'] ))
        logging.info("TITLE : {} , DATE : {} ".format(article2['title'], article2['date_p']))


        return score

    def scores_from_classifiers(self, classifier, features_id1, features_id2):
        score = classifier.get_score_id_id(features_id1.id, features_id2.id)
        score_tit = classifier.get_score_doc_doc(tok1=features_id1.tokenized_title , tok2=features_id2.tokenized_title)
        score_sum = classifier.get_score_doc_doc(tok1=features_id1.tokenized_summary , tok2=features_id2.tokenized_summary )
        score_sum_b = classifier.get_score_doc_doc(tok1=features_id1.tokenized_summaryb , tok2=features_id2.tokenized_summaryb)
        return score, score_tit, score_sum, score_sum_b


    def unique_words_diff(self, aggregator, features_id1, features_id2):
        cw_tot = aggregator.common_miss_words_doc(tok1=features_id1.tokenized_full_text , tok2=features_id2.tokenized_full_text)
        cw_tit = aggregator.common_miss_words_doc(tok1=features_id1.tokenized_title , tok2=features_id2.tokenized_title)
        cw_sum1 = aggregator.common_miss_words_doc(tok1=features_id1.tokenized_summary , tok2=features_id2.tokenized_summary)
        cw_sum_b = aggregator.common_miss_words_doc(tok1=features_id1.tokenized_summaryb , tok2=features_id2.tokenized_summaryb)
        return cw_tot, cw_tit, cw_sum1, cw_sum_b
