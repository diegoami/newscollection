from .summary_tfidf_strategy import SummaryTfidfStrategy

import logging

class SummaryFacade():

    def __init__(self, tfidfFacade, doc2vecFacade, **kwargs ):
        self.tfidfFacade = tfidfFacade
        self.doc2vecFacade = doc2vecFacade
        self.summaryStrategy = SummaryTfidfStrategy(tfidfFacade)



    def summarize(self, id, doc, title):

        return self.summaryStrategy.get_summary_sentences(id, doc)

    def summarize_text(self, doc, title):
        logging.debug("Entering summarize_text : title : {}".format(title))
        logging.debug("text : {}".format(doc))

        doc_bow = self.tfidfFacade.get_doc_bow(doc=doc, title=title)
        logging.debug("docbow : {}".format(str(doc_bow)))
        return self.summaryStrategy.get_sentences_from_bow(doc_bow , doc)