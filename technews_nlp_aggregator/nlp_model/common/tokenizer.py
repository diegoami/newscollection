


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
                logging.info("Processed  {} texts".format(len(texts)))
            return row


        logging.info("Tokenizing documents... this might take a while")
        logging.info("ArticleDF has {} rows ".format(len(articleDF)))
        #articleDF.apply(tokenize , axis=1)
        articleDF['article_txt'] = articleDF['title'].map(str)+".\n"+ articleDF['text']
        articleDF['article_tokens'] = articleDF['article_txt'].map(self.tokenize_fulldoc)

      #  for index, row in articleDF.iterrows():

      #      texts.append(self.tokenize_fulldoc(row['article_txt']))
     #       if (len(texts) % 100 == 0):
      #          logging.info("Processed  {} texts".format(len(texts)))
            #print(len(texts), len(articleDF['text']), len(articleDF['text'].tolist()))
        #return texts
        return articleDF['article_tokens']

    def tokenize_doc(self, title, document):
        return self.tokenize_fulldoc(title) + self.tokenize_fulldoc(document)

    def tokenize_fulldoc(self, all_doc):
        words = self.word_tokenizer.tokenize_fulldoc(all_doc)

        return words

    def clean_text(self, text):

        text = self.articles_cleaner.do_clean(text)
        text = self.sentence_tokenizer.clean_sentences(text)
        result = " ".join(text)
        return result


defaultTokenizer = DefaultTokenizer()