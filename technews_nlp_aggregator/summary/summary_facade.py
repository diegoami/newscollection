from .summary_tfidf_strategy import SummaryTfidfStrategy

import logging

class SummaryFacade():

    def __init__(self, tfidfFacade, doc2vecFacade, **kwargs ):
        self.tfidfFacade = tfidfFacade
        self.doc2vecFacade = doc2vecFacade
        self.summaryStrategy = SummaryTfidfStrategy(tfidfFacade)



    def summarize(self, id, doc, title='', threshold=0.8):

        return self.summaryStrategy.get_summary_sentences(id, doc, title, threshold)

    def summarize_text(self, doc, title, threshold=0.8):
        logging.debug("Entering summarize_text : title : {}".format(title))
        logging.debug("text : {}".format(doc))
        tokenized_doc = self.tfidfFacade.get_tokenized(doc=doc, title=title)
        doc_bow = self.tfidfFacade.get_doc_bow(tokenized_doc)
        logging.debug("docbow : {}".format(str(doc_bow)))
        return self.summaryStrategy.get_sentences_from_bow(bow=doc_bow , doc=doc, title=title, threshold=threshold)

    def full_text_summarize(self, id, doc, title='', threshold=0.8):
        sentences = self.summarize(id, doc, title, threshold)
        full_text = " ".join([x[1] for x in sentences if x[0] == 1])
        logging.debug("Full_text_summarize: {}".format(full_text))
        return full_text
