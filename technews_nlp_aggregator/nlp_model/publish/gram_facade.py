
BIGRAMS_PHRASER_FILENAME   = 'bigrams_phraser'
BIGRAMS_PHRASES_FILENAME   = 'bigrams_phrases'
TRIGRAMS_PHRASER_FILENAME   = 'trigrams_phraser'
TRIGRAMS_PHRASES_FILENAME   = 'trigrams_phrases'

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.models.phrases import Phraser, Phrases
class GramFacade():

    def __init__(self, model_dir):
        self.model_dir = model_dir

    def load_models(self):
        self.bigrams_phraser = Phraser.load(self.model_dir + '/' + BIGRAMS_PHRASER_FILENAME)
        self.trigrams_phraser = Phraser.load(self.model_dir + '/' + TRIGRAMS_PHRASER_FILENAME)

    def export_bigrams(self, docs):
         return  [self.bigrams_phraser[doc] for doc in  docs]

    def export_trigrams(self, bigrams):
        return [self.trigrams_phraser[bigram] for bigram in bigrams]


    def phrase(self, doc):
        bigrams = self.bigrams_phraser[doc]
        trigrams = self.trigrams_phraser[bigrams]
        return trigrams


    def create_model(self, doc_list):
        bigrams_phrases = Phrases(doc_list, min_count=5)
        bigrams_phraser = Phraser(bigrams_phrases)
        trigrams_phrases = Phrases(bigrams_phraser[doc_list], min_count=4)
        trigrams_phraser = Phraser(trigrams_phrases)
        bigrams_phraser.save(self.model_dir + '/' + BIGRAMS_PHRASER_FILENAME)
        trigrams_phraser.save(self.model_dir + '/' + TRIGRAMS_PHRASER_FILENAME)

