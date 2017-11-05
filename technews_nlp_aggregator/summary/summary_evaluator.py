class SummaryEvaluator():

    def __init__(self, tfidfFacade, doc2vecFacade):
        self.tfidfFacade = tfidfFacade
        self.doc2vecFacade = doc2vecFacade


    def evaluate(self, title,  test_sentences, article_id):
        test_text = " ".join(test_sentences)
        tfidf_score = self.tfidfFacade.compare_docs_to_id(title, test_text, article_id) * 100
        doc2vec_score = self.tfidfFacade.compare_docs_to_id(title, test_text, article_id) * 100
        return  ( tfidf_score + doc2vec_score ) / 2