


from . import SimpleSentenceTokenizer, TechArticlesSentenceTokenizer

from . import TechArticlesWordTokenizer
from . import TechArticlesCleaner

import logging


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class DefaultTokenizer:

    def __init__(self, sentence_tokenizer=None, word_tokenizer=None):
        self.sentence_tokenizer = TechArticlesSentenceTokenizer() if not sentence_tokenizer else sentence_tokenizer

        self.word_tokenizer = TechArticlesWordTokenizer() if not word_tokenizer else word_tokenizer
        self.articles_cleaner = TechArticlesCleaner()

    def tokenize_ddf(self, articleDF):

        texts = []


        def tokenize (row):
            texts.append(self.tokenize_doc(row['title'],row['text']))

            if (len(texts) % 100 == 0):
                print("Processed  {}".format(len(texts)))
            return row


        logging.info("Tokenizing documents... this might take a while")

        articleDF.apply(tokenize , axis=1)
        return texts

    def tokenize_doc(self, title, document):
        return self.word_tokenizer.tokenize_fulldoc(title) + self.word_tokenizer.tokenize_fulldoc(document)

    def tokenize_fulldoc(self, all_doc):
        words = self.word_tokenizer.tokenize_fulldoc(all_doc)
        return words

    def clean_text(self, text):

        text = self.articles_cleaner.do_clean(text)
        text = self.sentence_tokenizer.clean_sentences(text)
        return "".join(text)


defaultTokenizer = DefaultTokenizer()