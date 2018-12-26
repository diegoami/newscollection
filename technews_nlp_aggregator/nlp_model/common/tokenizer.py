


from . import  TechArticlesSentenceTokenizer

from . import TechArticlesWordTokenizer
from . import TechArticlesCleaner
from . import TechArticlesPreprocessor

import logging





class DefaultTokenizer:

    def __init__(self, sentence_tokenizer=None, word_tokenizer=None, preprocessor=None):
        self.sentence_tokenizer = TechArticlesSentenceTokenizer() if not sentence_tokenizer else sentence_tokenizer
        self.preprocessor = TechArticlesPreprocessor() if not preprocessor else preprocessor
        self.word_tokenizer = TechArticlesWordTokenizer(self.preprocessor) if not word_tokenizer else word_tokenizer
        self.articles_cleaner = TechArticlesCleaner()



    def tokenize_ddf(self, articleDF):

        texts = []


        def tokenize (row):
            texts.append(self.tokenize_doc(row['title'],row['text']))

            if (len(texts) % 100 == 0):
                logging.info("Processed  {} texts".format(len(texts)))
            return row


        logging.info("Tokenizing documents... this might take a while")
        logging.info("ArticleDF has {} rows ".format(len(articleDF)))

        articleDF['article_txt'] = articleDF['title'].map(str)+".\n"+ articleDF['text']
        articleDF['article_tokens'] = articleDF['article_txt'].apply(lambda x: self.tokenize_fulldoc(x, do_log=True))


        return articleDF['article_tokens']

    def tokenize_doc(self, title, doc, do_lemma=True):
        if title:
            return self.tokenize_fulldoc(title + ". \n" + doc, do_lemma=do_lemma)
        else:
            return self.tokenize_fulldoc(doc, do_lemma=do_lemma)

    def tokenize_fulldoc(self, all_doc, do_lemma=True, do_log=False):
        words = self.word_tokenizer.tokenize_fulldoc(all_doc, do_lemma=do_lemma, do_log=do_log)

        return words

    def clean_text(self, text):

        text = self.articles_cleaner.do_clean(text)
        text = self.sentence_tokenizer.clean_sentences(text)
        result = " ".join(text)
        return result


defaultTokenizer = DefaultTokenizer()