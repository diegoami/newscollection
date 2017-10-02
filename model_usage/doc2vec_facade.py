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



MIN_FREQUENCY = 3
MODEL_FILENAME   = 'doc2vec'

class Doc2VecFacade:

    def __init__(self, model_dir):
        self.model_dir = model_dir


    def load_models(self):
        self.model = Doc2Vec.load(self.model_dir + MODEL_FILENAME)


    def get_related_articles(self, doc, n):
        wtok = [i for i in word_tokenize(doc.lower())]
        infer_vector = self.model.infer_vector(wtok)

        similar_documents = self.model.docvecs.most_similar([infer_vector], topn=n)
        print(similar_documents)
        return similar_documents
