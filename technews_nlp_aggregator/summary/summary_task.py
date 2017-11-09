import time
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer
class SummaryTask():
    def __init__(self, title, doc, article_id, percentage):
        self.title = title
        self.doc = doc
        self.article_id = article_id
        self.percentage = percentage

        self.sentences = defaultTokenizer.sentence_tokenizer.sent_tokenize(self.doc)
        self.result = None


    def execute(self, evaluator):
        ss_sentences = self.sentences
        self.removed_sentences = []
        done = False
        start_time = time.time()
        # your code

        while not done:
            best_index, best_result = None, 0
            for index, sentence in enumerate(ss_sentences ):
                loop_sentences = ss_sentences[:index]+ss_sentences[index+1:]
                excluded_sentence = ss_sentences[index]
                eval_result = evaluator.evaluate(self.title, loop_sentences, excluded_sentence ,self.article_id)
                if (eval_result > best_result ):
                    best_index, best_result = index, eval_result
            self.removed_sentences.append(ss_sentences[best_index])

            ss_sentences = ss_sentences[:best_index]+ss_sentences[best_index+1:]
            elapsed_time = time.time() - start_time
            if (best_result < self.percentage) or len(ss_sentences) == 0 or elapsed_time> 30:

                self.summary_sentences = [ss for ss in ss_sentences if len(ss.strip()) > 0]
                done = True

    def get_summary_sentences(self):
        return self.summary_sentences
