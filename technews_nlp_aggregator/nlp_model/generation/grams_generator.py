from gensim.models.phrases import Phraser, Phrases

BIGRAMS_PHRASER_FILENAME   = 'bigrams_phraser'
BIGRAMS_PHRASES_FILENAME   = 'bigrams_phrases'
TRIGRAMS_PHRASER_FILENAME   = 'trigrams_phraser'
TRIGRAMS_PHRASES_FILENAME   = 'trigrams_phrases'

class GramsGenerator:
    def __init__(self, model_dir):
        self.model_dir = model_dir

    def create_model(self, doc_list):
        bigrams_phrases = Phrases(doc_list, min_count=5)
        bigrams_phraser = Phraser(bigrams_phrases)
        trigrams_phrases = Phrases(bigrams_phraser[doc_list], min_count=4)
        trigrams_phraser = Phraser(trigrams_phrases)
        bigrams_phraser.save(self.model_dir + '/' + BIGRAMS_PHRASER_FILENAME)
        trigrams_phraser.save(self.model_dir + '/' + TRIGRAMS_PHRASER_FILENAME)

