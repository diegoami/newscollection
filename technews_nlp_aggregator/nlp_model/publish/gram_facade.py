
BIGRAMS_PHRASER_FILENAME   = 'bigrams_phraser'
BIGRAMS_PHRASES_FILENAME   = 'bigrams_phrases'
TRIGRAMS_PHRASER_FILENAME   = 'trigrams_phraser'
TRIGRAMS_PHRASES_FILENAME   = 'trigrams_phrases'
BIGRAMS_PICKLE  = 'trigrams.p'
TRIGRAMS_PICKLE = 'bigrams.p'




from gensim.models.phrases import Phraser, Phrases
class GramFacade():

    def __init__(self, model_dir, min_count_bigrams=8, min_count_trigrams=7):
        self.model_dir = model_dir
        self.min_count_bigrams=min_count_bigrams
        self.min_count_trigrams=min_count_trigrams

    def load_models(self):
        self.bigrams_phraser = Phraser.load(self.model_dir + '/' + BIGRAMS_PHRASER_FILENAME)
        self.trigrams_phraser = Phraser.load(self.model_dir + '/' + TRIGRAMS_PHRASER_FILENAME)

    def load_phrases(self):
        self.bigrams_phrases = Phrases.load(self.model_dir + '/' + BIGRAMS_PHRASES_FILENAME)
        self.trigrams_phrases = Phrases.load(self.model_dir + '/' + TRIGRAMS_PHRASES_FILENAME)

    def export_bigrams(self, docs):
         return  [self.bigrams_phraser[doc] for doc in  docs]

    def export_trigrams(self, bigrams):
        return [self.trigrams_phraser[bigram] for bigram in bigrams]


    def phrase(self, doc):
        bigrams = self.bigrams_phraser[doc]
        trigrams = self.trigrams_phraser[bigrams]
        return trigrams


    def create_model(self, doc_list):
        self.bigrams_phrases = Phrases(doc_list, min_count=self.min_count_bigrams)
        self.bigrams_phraser = Phraser(self.bigrams_phrases)
        self.trigrams_phrases = Phrases(self.bigrams_phraser[doc_list], min_count=self.min_count_trigrams)
        self.trigrams_phraser = Phraser(self.trigrams_phrases)
        self.bigrams_phraser.save(self.model_dir + '/' + BIGRAMS_PHRASER_FILENAME)
        self.trigrams_phraser.save(self.model_dir + '/' + TRIGRAMS_PHRASER_FILENAME)
        self.bigrams_phrases.save(self.model_dir + '/' + BIGRAMS_PHRASES_FILENAME)
        self.trigrams_phrases.save(self.model_dir + '/' + TRIGRAMS_PHRASES_FILENAME)

    def words_not_in_vocab(self, tok_doc, threshold):
        word_not_in_doc =set([ x for x in tok_doc if self.trigrams_phrases.vocab[str.encode(x)] < threshold ])
        return word_not_in_doc
