from gensim.models.phrases import Phraser


class TechArticlesPhraser:

    def phrase_doc(self, doc_lists):
        bigram = Phraser(doc_lists)
        return bigrams