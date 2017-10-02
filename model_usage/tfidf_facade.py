
import json

MIN_FREQUENCY = 3
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'

from gensim import corpora, models, similarities

import os

from gensim.corpora import MmCorpus
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class TfidfFacade:
    def __init__(self, model_dir):
        self.model_dir = model_dir

    def load_models(self):
        self.dictionary = corpora.Dictionary.load(self.model_dir + self.dict_filename)  # store the dictionary, for future reference
        self.corpus = MmCorpus(self.model_dir + self.corpus_filename)
        self.lsi = models.LsiModel.load(self.model_dir + self.lsi_filename)
        self.index = similarities.MatrixSimilarity.load(self.model_dir + self.index_filename)  # transform corpus to LSI space and index it


    def get_vec(self,doc):
        vec_bow = self.dictionary.doc2bow(doc.lower().split())
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def get_related_articles(self, doc, n):
        vec_lsi = self.get_vec(doc)
        sims = self.index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return sims