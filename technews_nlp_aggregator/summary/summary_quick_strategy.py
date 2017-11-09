import time
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer
class SummaryQuickStrategy():
    def __init__(self, doc, sentences, article_id, tfidfFacade, doc2vecFacade):
        self.doc = doc
        self.article_id = article_id


        self.tfidfFacade = tfidfFacade
        self.doc2vecFacade = doc2vecFacade
        self.sentences = sentences
        self.result = None

        self.min_sentences = 2
        self.min_percentage = 0.2
        self.percentage = 0.5

        self.max_sentences = 8
        self.max_percentage = 0.8

    def get_scores(self):
        tfidf_scores = self.tfidfFacade.compare_sentences_to_id(self.sentences, self.article_id)
        doc2vec_scores = self.doc2vecFacade.compare_sentences_to_id(self.sentences, self.article_id)
        averaged_scores = ( tfidf_scores +  doc2vec_scores ) / 2
        #averaged_scores = (t_score + d_score )  * 50 for t_score, d_score in zip(tfidf_scores, doc2vec_scores )

        return averaged_scores

    def get_sentences(self, scores, sentences):
        how_many_sentences = max(self.min_sentences, int(len(scores) * self.min_percentage))
        how_many_sentences = min(self.max_sentences, how_many_sentences, int(len(scores) * self.max_percentage))


        scores_argsort = np.argsort(-scores)
        index_to_add = scores_argsort[:how_many_sentences].tolist()
        scores_l = scores.tolist()
        sentences_data = []

        for index, score in enumerate(scores_l):
            sentences_data.append({
                "score": score,
                "sentence": sentences[index],
                "highlighted": (score > self.percentage) or index in index_to_add

            })
        return sentences_data
