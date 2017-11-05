import time
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer
class SummaryQuickTask():
    def __init__(self, title, doc, article_id, tfidfFacade, doc2vecFacade):
        self.title = title
        self.doc = doc
        self.article_id = article_id


        self.sentences = defaultTokenizer.sentence_tokenizer.process(self.title, self.doc)
        self.tfidfFacade = tfidfFacade
        self.doc2vecFacade = doc2vecFacade
        self.result = None


    def get_scores(self):
        self.scores = self.tfidfFacade.compare_sentences_to_id(self.sentences, self.article_id)
        return self.scores

    def get_summary_sentences(self):
        return self.summary_sentences
