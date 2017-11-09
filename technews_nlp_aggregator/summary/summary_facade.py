from .summary_task import SummaryTask
from .summary_quick_task import SummaryQuickTask
from .summary_evaluator import SummaryEvaluator
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer
import logging
import numpy as np
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
class SummaryFacade():

    def __init__(self, tfidfFacade, doc2vecFacade, percentage = 55, min_sentences = 2, max_sentences = 8, min_percentage = 0.2, max_percentage = 0.5 ):
        self.tfidfFacade = tfidfFacade
        self.doc2vecFacade = doc2vecFacade
        self.evaluator = SummaryEvaluator(tfidfFacade, doc2vecFacade)
        self.percentage = percentage
        self.min_sentences = min_sentences
        self.max_sentences = max_sentences
        self.min_percentage = min_percentage
        self.max_percentage = max_percentage

    def summarize_intensive(self, title, doc, article_id, percentage):
        summaryTask = SummaryTask(title, doc, article_id, percentage)
        summaryTask.execute(self.evaluator)
        sentences_zipped = []
        for index, sentence in enumerate(summaryTask.sentences):
            sentences_zipped.append((sentence not in summaryTask.removed_sentences, sentence))
        return sentences_zipped

    def summarize(self, title, doc, article_id):
        sentences = defaultTokenizer.sentence_tokenizer.process( doc)

        summaryQuickTask = SummaryQuickTask(doc, sentences, article_id, self.tfidfFacade, self.doc2vecFacade)
        scores = summaryQuickTask.get_scores()
        how_many_sentences = max(self.min_sentences, int(len(scores) * self.min_percentage ) )
        how_many_sentences = min(self.max_sentences, how_many_sentences , int(len(scores) * self.max_percentage) )
        logging.info("How many sentence = " + str(how_many_sentences ))

        scores_argsort = np.argsort(-scores)
        index_to_add = scores_argsort[:how_many_sentences].tolist()
        scores_l = scores.tolist()
        sentences_data = []
        logging.info("Score_l = "+str(scores_l))
        for index, score in enumerate(scores_l):
            sentences_data.append({
                "score" : score,
                "sentence" : sentences[index],
                "highlighted" : (score > self.percentage) or index in index_to_add

            })
        for sentence_part in sentences_data:
            logging.info(sentence_part)

        return sentences_data
