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

excl_4 = ['-','@','\'s','``','\'\'' ,'&', '\'', '`', '!', '[', ']', '‘', '=', '…', '$' , '%', '<', '>', '"', '/', '\n']

not_excl_1 =['need', 'using', 'more', 'new', '$', 'company', 'out','people','google','time', 'data', 'app', 'game', 'service', 'video'
             'companies', 'apple', 'over', 'million', 'first', 'year', 'even', 'most', 'much', 'users', 'well', 'today', 'technology', 'last', 'want'
            ,'many','world', 'work','ai', 'still', 'own', 'help', 'team','years', 'back', 'games','market', 'uber',  'better', 'part', 'product', 'facebook', 'might',
            'very', 'good', 'think', 'vr', 've','next', '2017', 'something', 'including', 'amazon', 'tech',
             'business','startup', 'billion', 'since', 'watch', 'mobile']
excl_5 = ['’s', '’ll', '’re', "'m", '#' , 'n’t']


excl_all = set(excl_1 + excl_2 + excl_3 + excl_4 + excl_5)

class TechArticlesWordTokenizer:
    def __init__(self):
        all_stopwords = STOP_WORDS.union(excl_all).union(punctuation)
        for word in all_stopwords:
            spacy_nlp.vocab[word].is_stop = True


    def tokenize_sentences(self, all_sentences):
        tokenized_sentences = []
        for sentence in all_sentences:
            tokenized_sentences.append(self.tokenize_fulldoc(sentence))
        return tokenized_sentences

    def tokenize_fulldoc(self, doc):
        tok_doc = spacy_nlp(doc.lower())
        return [word.text for word in tok_doc if not word.is_stop]

    def tokenize_doc(self, title, document):
        return self.tokenize_fulldoc(title+".\n"+document)