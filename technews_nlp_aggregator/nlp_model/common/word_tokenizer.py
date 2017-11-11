import logging
from string import punctuation

from technews_nlp_aggregator.nlp_model.spacy import spacy_nlp
from spacy.en.word_sets import STOP_WORDS
import logging




excl_1 = [',', 'the', '.', 'to', 'and', 'a', 'of', '’', 'in', 'that', 'it', 'is', 'for', 'with', 'on', 'you', 'as', '“', '”',  'this', 'but', 'from',  'its', 'at', 'can', 'an',  'we',   'by',   'your', 'or',  'they', '—', ':', '(', ')', 'their', 'like', 'which', 'not', 'one', 'also',]
excl_2 = ['about', 'if', 'what', 'up', 'so', 'there', 'all', 'he', 'other', 'some', 'just', 'when', 'into',  'how', 'now', 'than', 'them',  'while', 'who', 'our',   'get', 're', 'could',  'use', 'would', 'way', 'only', 'make', '?', 'his']

excl_3 = [  'these',  'after', 'us', 'no', 'where', 'through', 'those',  'my', 'don', 'two',  'because',  'll', 'same', 'around',  '–',  'then', 'both', 'any', ';',  'before',   'here', 'able',  'down', 'she', 'her', 're', ]

excl_4 = ['-','@','\'s','``','\'\'' ,'&', '\'', '`', '!', '[', ']', '‘', '=', '…',
          #'$' , '£', '€',
          '%', '<', '>', '"', '/', '\n', '\s', '\t', ' ', '\r' , '\xa0', '...']

excl_5 = ['’s', '’ll', '’re', "'m", '#' , 'n’t', "'s", '--', "'"]



excl_all = set(excl_1 + excl_2 + excl_3 + excl_4 + excl_5  )
exc_all = set()

class TechArticlesWordTokenizer:
    def __init__(self, preprocessor):
        all_stopwords = STOP_WORDS.union(excl_all).union(punctuation)
        #all_stopwords = STOP_WORDS.union(punctuation)
        for word in all_stopwords:
            spacy_nlp.vocab[word].is_stop = True
        self.preprocessor = preprocessor
        self.count = 0

    def tokenize_sentences(self, all_sentences):
        tokenized_sentences = []
        for sentence in all_sentences:
            tokenized_sentences.append(self.tokenize_fulldoc(sentence))
        return tokenized_sentences

    def simple_tokenize(self, doc):
        tok_doc = spacy_nlp(doc.lower())
        return [token.text for token in tok_doc]

    def tokenize_fulldoc(self, doc):
        if self.preprocessor:
            doc = self.preprocessor.process(doc)
        tok_doc = spacy_nlp(doc)
        self.count += 1
        if (self.count % 100 == 0):
            logging.info("Processed {} documents ".format(self.count))
        return [word.lemma_ for word in tok_doc if not word.is_stop and not word.is_space ]

    def tokenize_doc(self, title, document):
        return self.tokenize_fulldoc(title+".\n"+document)

