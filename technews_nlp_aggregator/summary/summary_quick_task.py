import time
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer
class SummaryQuickTask():
    def __init__(self, doc, sentences, article_id, tfidfFacade, doc2vecFacade):
        self.doc = doc
        self.article_id = article_id


        self.tfidfFacade = tfidfFacade
        self.doc2vecFacade = doc2vecFacade
        self.sentences = sentences
        self.result = None


    def get_scores(self):
        tfidf_scores = self.tfidfFacade.compare_sentences_to_id(self.sentences, self.article_id)
        doc2vec_scores = self.doc2vecFacade.compare_sentences_to_id(self.sentences, self.article_id)
        averaged_scores = ( tfidf_scores +  doc2vec_scores ) / 2
        #averaged_scores = (t_score + d_score )  * 50 for t_score, d_score in zip(tfidf_scores, doc2vec_scores )

        return averaged_scores

    def get_summary_sentences(self):
        return self.summary_sentences
