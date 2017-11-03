from technews_nlp_aggregator.nlp_model.spacy import spacy_nlp

class ArticleLemmer():

    def process_doc(self, doc):
        spacy_nlp(doc)