import json


from gensim import corpora, models, similarities

import os

from gensim.corpora import MmCorpus

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string

from os import listdir
from os.path import isfile, join
from gensim.models.doc2vec import TaggedDocument
from datetime import datetime
import json
from gensim.models import Doc2Vec
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            wtok = [i for i in word_tokenize(doc)]
            tags = [self.labels_list[idx]]

            yield TaggedDocument(words=wtok, tags=tags)


class Doc2VecClassifier:

    def __init__(self, model_filename):
        self.model_filename = model_filename


    def load_models(self):
        self.model = Doc2Vec.load(self.model_filename)

    def update_models(self, texts, urls):

        it = LabeledLineSentence(texts, urls)

        self.model = Doc2Vec(size=300, window=10, min_count=5, workers=11, alpha=0.025, min_alpha=0.025,
                        iter=10)  # use fixed learning rate
        self.model.build_vocab(it)

        logging.info("Starting to train......")

        # for epoch in range(10):
        #    logging.info("On epoch "+str(epoch))
        # model.train(it)
        # model.alpha -= 0.002 # decrease the learning rate
        # model.min_alpha = model.alpha # fix the learning rate, no deca
        self.model.train(it, total_examples=self.model.corpus_count, epochs=self.model.iter)
        #   logging.info("Finished training epoch " + str(epoch))

        logging.info("Training completed, saving to  " + self.model_filename)
        self.model.save(self.model_filename)




    def get_related_articles(self, doc, n):
        wtok = [i for i in word_tokenize(doc)]
        infer_vector = self.model.infer_vector(wtok)

        similar_documents = self.model.docvecs.most_similar([infer_vector], topn=n)
        print(similar_documents)
        return similar_documents

    def do_print_related(self, doc):
        logging.debug(" ============ BASE ARTICLE  ========================")
        logging.debug(doc)
        logging.debug(" ============ RELATED TITLES =======================")
        related_articles = self.get_related_articles(doc,10)
        for article in related_articles:
            logging.debug(article)


