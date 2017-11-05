from .summary_task import SummaryTask
from .summary_quick_task import SummaryQuickTask
from .summary_evaluator import SummaryEvaluator
import logging
import numpy as np
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
class SummaryFacade():

    def __init__(self, tfidfFacade, doc2vecFacade):
        self.tfidfFacade = tfidfFacade
        self.doc2vecFacade = doc2vecFacade
        self.evaluator = SummaryEvaluator(tfidfFacade, doc2vecFacade)

    def summarize_intensive(self, title, doc, article_id, percentage):
        summaryTask = SummaryTask(title, doc, article_id, percentage)
        summaryTask.execute(self.evaluator)


        sentences_zipped = []
        for index, sentence in enumerate(summaryTask.sentences):
            sentences_zipped.append((sentence not in summaryTask.removed_sentences, sentence))
        return sentences_zipped

    def summarize(self, title, doc, article_id, percentage):
        summaryQuickTask = SummaryQuickTask(title, doc, article_id, self.tfidfFacade, self.doc2vecFacade)
        scores = summaryQuickTask.get_scores() * 100
        how_many_sentences = max(2, len(scores) // 5 )
        scores_argsort = np.argsort(-scores)

        index_to_add = scores_argsort[:how_many_sentences].tolist()

        sentences_zipped = []
        for index, score in enumerate(scores):
            sentences_zipped.append((score > percentage or index in index_to_add , summaryQuickTask.sentences[index]))
        return sentences_zipped
