


from nltk.tokenize import sent_tokenize, word_tokenize
MIN_FREQUENCY = 3
from . import SimpleSentenceTokenizer, TechArticlesSentenceTokenizer
from .token_excluder import TechArticlesTokenExcluder, SimpleTokenExcluder
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class DefaultTokenizer:

    def __init__(self, sentence_tokenizer=None, token_excluder=None):
        self.sentence_tokenizer = TechArticlesSentenceTokenizer() if not sentence_tokenizer else sentence_tokenizer
        self.token_excluder = TechArticlesTokenExcluder() if not token_excluder else token_excluder

    def tokenize_ddf(self, articleDF):
        documents = articleDF['text'].tolist()
        titles = articleDF['title'].tolist()
        logging.info("Tokenizing documents... this might take a while")
        texts = [self.tokenize_doc(title, document) for title, document in zip(titles, documents)]
        logging.info("Done with tokenizing")
        # remove words that appear only once

        return texts

    def tokenize_doc(self, title, document):
        all_sentences = self.sentence_tokenizer.process(title, document)

        tokenized_sentences = []
        for sentence in all_sentences:
            tokenized_sentences.append([word for word in word_tokenize(sentence.lower()) ])

        words = []
        for tokenized_sentence in tokenized_sentences:
            for token in tokenized_sentence:
                if self.token_excluder.is_token_allowed(token):
                    words.append(token)

        return words

