import logging
from string import punctuation
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.nlp_model.spacy import spacy_nlp
from spacy.en.word_sets import STOP_WORDS
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



excl_1 = [',', 'the', '.', 'to', 'and', 'a', 'of', '’', 'in', 'that', 's', 'it', 'is', 'for', 'with', 'on', 'you', 'as', '“', '”', 'be', 'this', 'but', 'are', 'from',  'its', 'at', 'can', 'an', 'have', 'we', 'has', 'i', 'by', 't',  'your', 'or', 'was', 'they', '—', ':', '(', ')', 'their', 'like', 'which', 'not', 'one', 'also','will']
excl_2 = ['about', 'if', 'what', 'up', 'so', 'there', 'all', 'he', 'said', 'other', 'some', 'just', 'when', 'into',  'been', 'how', 'now', 'than', 'them',  'said',  'while', 'who', 'our',   'get', 're', 'could',  'use', 'would', 'way', 'only', 'make', '?', 'his']

excl_3 = [ 'do', 'these', 'says', 'were', 'had',  'see', 'after', 'us', 'no', 'where', 'may', 'through', 'those',  'my', 'don', 'two',  'because',  'll', 'same', 'take',  'around',  'made',  '–',  'then', 'both', 'any', ';',  'before', 'going', 'being',  'here', 'able',  'down', 'lot', 'right', 'she', 'her', 're', 'm', 've', 'd']

excl_4 = ['-','@','\'s','``','\'\'' ,'&', '\'', '`', '!', '[', ']', '‘', '=', '…', '$' , '%', '<', '>', '"', '/', '\n', '\s', '\t', ' ', '\r' , '\xa0', '...']

excl_5 = ['’s', '’ll', '’re', "'m", '#' , 'n’t', "'s", '--', "'"]
excl_6 = [" "*x for x in range(1,12)]


excl_all = set(excl_1 + excl_2 + excl_3 + excl_4 + excl_5 + excl_6 )

class TechArticlesWordTokenizer:
    def __init__(self):
        all_stopwords = STOP_WORDS.union(excl_all).union(punctuation)
        #all_stopwords = STOP_WORDS.union(punctuation)
        for word in all_stopwords:
            spacy_nlp.vocab[word].is_stop = True


    def tokenize_sentences(self, all_sentences):
        tokenized_sentences = []
        for sentence in all_sentences:
            tokenized_sentences.append(self.tokenize_fulldoc(sentence))
        return tokenized_sentences

    def simple_tokenize(self, doc):
        tok_doc = spacy_nlp(doc.lower())
        return [token.text for token in tok_doc]

    def tokenize_fulldoc(self, doc):
        tok_doc = spacy_nlp(doc)
        #return [word.text.strip() for word in tok_doc if not word.is_stop and len(word.text.strip()) > 0]
        return [word.lemma_ for word in tok_doc if not word.is_stop and not word.is_space ]

    def tokenize_doc(self, title, document):
        return self.tokenize_fulldoc(title+".\n"+document)

