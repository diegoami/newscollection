


from . import SimpleSentenceTokenizer, TechArticlesSentenceTokenizer
from . import TechArticlesTokenExcluder, SimpleTokenExcluder
from . import TechArticlesWordTokenizer
from . import TechArticlesCleaner
import logging


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class DefaultTokenizer:

    def __init__(self, sentence_tokenizer=None, token_excluder=None, word_tokenizer=None):
        self.sentence_tokenizer = TechArticlesSentenceTokenizer() if not sentence_tokenizer else sentence_tokenizer
        self.token_excluder = TechArticlesTokenExcluder() if not token_excluder else token_excluder
        self.word_tokenizer = TechArticlesWordTokenizer() if not word_tokenizer else word_tokenizer
        self.articles_cleaner = TechArticlesCleaner()

    def tokenize_ddf(self, articleDF):
        documents = articleDF['text'].tolist()
        titles = articleDF['title'].tolist()
        logging.info("Tokenizing documents... this might take a while")
        texts = []

        for title, document in zip(titles, documents):
            tokdoc = self.tokenize_doc(title, document)
            if tokdoc:
                texts.append(tokdoc)
        logging.info("Done with tokenizing")
        # remove words that appear only once

        return texts

    def tokenize_doc(self, title, document):
        all_sentences = self.sentence_tokenizer.process(title, document)
        if all_sentences:

            tokenized_sentences = self.word_tokenizer.tokenize_sentences(all_sentences)
            words = []
            for tokenized_sentence in tokenized_sentences:
                for token in tokenized_sentence:
                    if self.token_excluder.is_token_allowed(token):
                        words.append(token)

            return words
        else:
            return None

    def clean_text(self, text):

        text = self.articles_cleaner.do_clean(text)
        text = self.sentence_tokenizer.clean_sentences(text)
        return "\n".join(text)


defaultTokenizer = DefaultTokenizer()