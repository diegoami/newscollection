MIN_FREQUENCY = 3
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'

import logging

from gensim import corpora, models, similarities
from gensim.corpora import MmCorpus
from nltk.tokenize import word_tokenize
from technews_nlp_aggregator.nlp_model.common import Tokenizer
import pandas as pd

import datetime

from technews_nlp_aggregator.nlp_model.publish.clf_facade import ClfFacade

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

tokenizer = Tokenizer()
class TfidfFacade(ClfFacade):

    def __init__(self, model_dir, article_loader):
        self.model_dir = model_dir
        self.article_loader = article_loader

    def load_models(self):
        self.dictionary = corpora.Dictionary.load(self.model_dir + '/'+DICTIONARY_FILENAME)  # store the dictionary, for future reference
        self.corpus = MmCorpus(self.model_dir + '/'+ CORPUS_FILENAME )
        self.lsi = models.LsiModel.load(self.model_dir + '/'+ LSI_FILENAME)
        self.index = similarities.MatrixSimilarity.load(self.model_dir + '/'+ INDEX_FILENAME)  # transform corpus to LSI space and index it


    def get_vec(self,doc):
        words = tokenizer.tokenize_doc('', doc)
        vec_bow = self.dictionary.doc2bow(words)
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def get_vec_docid(self, id):

        vec_bow = self.corpus[id]
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def get_related_sims_docid(self, id, n):
        vec_lsi = self.get_vec_docid(id)
        sims = self.index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return sims[:n]


    def get_related_sims(self, doc, n):
        vec_lsi = self.get_vec(doc)
        sims = self.index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return sims[:n]


    def get_related_articles_and_score_doc(self, doc, n):
        sims = self.get_related_sims(doc, n)
        related_articles = sims
        return related_articles[:n]

    def get_related_articles_and_score_docid(self,  docid, n=10000, max=15):

        docrow = self.article_loader.articlesDF.loc[docid]
        #print(docrow["title"])

        similar_documents = self.get_related_sims_docid(docid , n)
        #print(similar_documents)
        df_similar_docs = self.enrich_with_score(similar_documents,200,docrow['date_p'])

        return df_similar_docs.iloc[:max,:]



