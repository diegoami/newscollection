
BIGRAMS_PHRASER_FILENAME   = 'bigrams_phraser'
BIGRAMS_PHRASES_FILENAME   = 'bigrams_phrases'
TRIGRAMS_PHRASER_FILENAME   = 'trigrams_phraser'
TRIGRAMS_PHRASES_FILENAME   = 'trigrams_phrases'

from gensim.models.phrases import Phraser, Phrases
class GramFacade():

    def __init__(self, model_dir):
        self.model_dir = model_dir

        self.bigrams_phraser = Phraser.load(model_dir+'/'+BIGRAMS_PHRASER_FILENAME )
       # self.bigrams_phrases = Phraser.load(model_dir+'/'+BIGRAMS_PHRASES_FILENAME )
        self.trigrams_phraser = Phraser.load(model_dir+'/'+TRIGRAMS_PHRASER_FILENAME )
       # self.trigrams_phrases  = Phraser.load(model_dir+'/'+TRIGRAMS_PHRASES_FILENAME )



    def export_bigrams(self, docs):
         return  [self.bigrams_phraser[doc] for doc in  docs]

    def export_trigrams(self, bigrams):
        return [self.trigrams_phraser[bigram] for bigram in bigrams]


    def phrase(self, doc):
        bigrams = self.bigrams_phraser[doc]
        trigrams = self.trigrams_phraser[bigrams]
        return trigrams