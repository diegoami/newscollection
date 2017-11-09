from .summary_heavy_strategy import SummaryHeavyStrategy
from .summary_quick_strategy import SummaryQuickStrategy
from .summary_tfidf_strategy import SummaryTfidfStrategy

from .summary_evaluator import SummaryEvaluator
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer
import logging
import numpy as np
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
class SummaryFacade():

    def __init__(self, tfidfFacade, doc2vecFacade, **kwargs ):
        self.tfidfFacade = tfidfFacade
        self.doc2vecFacade = doc2vecFacade
        self.summaryStrategy = SummaryTfidfStrategy(tfidfFacade)



    def summarize(self, id, title, text ):
        return self.summaryStrategy.get_summary_sentences(id, text)