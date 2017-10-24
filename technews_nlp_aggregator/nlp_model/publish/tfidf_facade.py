MIN_FREQUENCY = 3
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'

import logging

from gensim import corpora, models, similarities
from gensim.corpora import MmCorpus
from nltk.tokenize import word_tokenize
from technews_nlp_aggregator.nlp_model.common import DefaultTokenizer
import pandas as pd
from .tfidf_matrix_wrapper import TfidfMatrixWrapper
import datetime
import numpy as np
from . import ClfFacade

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class TfidfFacade(ClfFacade):

    def __init__(self, model_dir, article_loader, tokenizer=None):
        self.model_dir = model_dir
        self.article_loader = article_loader
        self.name = 'TFIDF-V1-500'
        self.tokenizer = DefaultTokenizer() if not tokenizer else tokenizer

    def load_models(self):
        self.dictionary = corpora.Dictionary.load(self.model_dir + '/'+DICTIONARY_FILENAME)  # store the dictionary, for future reference
        self.corpus = MmCorpus(self.model_dir + '/'+ CORPUS_FILENAME )
        self.lsi = models.LsiModel.load(self.model_dir + '/'+ LSI_FILENAME)
        self.matrix_wrapper = TfidfMatrixWrapper(similarities.MatrixSimilarity.load(self.model_dir + '/'+ INDEX_FILENAME))  # transform corpus to LSI space and index it


    def get_vec(self,doc):
        words = self.tokenizer.tokenize_doc('', doc)
        vec_bow = self.dictionary.doc2bow(words)
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def get_vec_docid(self, id):

        vec_bow = self.corpus[id]
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def get_related_sims_docid(self, id, n):
        vec_lsi = self.get_vec_docid(id)
        sims = self.matrix_wrapper[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return sims[:n]

    def get_related_articles_and_score_doc(self, doc, start=None, end=None):
        vec_lsi = self.get_vec(doc)
        if (start and end):
            interval_condition = (self.article_loader.articlesDF['date_p'] >= start) & (self.article_loader.articlesDF['date_p'] <= end)
            scores = self.matrix_wrapper[(vec_lsi, interval_condition) ]
            articlesFilteredDF = self.article_loader.articlesDF[interval_condition ]
        else:
            scores = self.matrix_wrapper[(vec_lsi,None)]
            articlesFilteredDF = self.article_loader.articlesDF
        args_scores = np.argsort(-scores)
        return args_scores, scores[args_scores]


    def get_related_articles_from_to(self, doc,  start, end):
        articlesFoundDF, scores = self.get_related_articles_and_score_doc(doc, start, end )

        return articlesFoundDF, scores

    def get_related_articles_and_score_url(self,  url):


        url_condition = self.article_loader.articlesDF['url'] == url
        vec_lsi = self.get_vec_docid(id)
        sims = self.matrix_wrapper[vec_lsi]
        docrow = self.article_loader.articlesDF[url_condition]
        if (len(docrow) > 0):
            docid = docrow.index[0]
            vec_lsi = self.get_vec_docid(id)
            scores = self.matrix_wrapper[(vec_lsi,None)]
            args_scores = np.argsort(-scores)
            return args_scores, scores[args_scores]
        else:
            return None, None




    def compare_articles_from_dates(self,  start, end, thresholds):
        articles_and_sim = {}
        docs_of_day = self.article_loader.articles_in_interval(start, end)
        dindex = docs_of_day.index
        for id, row in docs_of_day.iterrows():
            vec_lsi = self.get_vec_docid(id)
            sims = self.index[vec_lsi]
            for other_id in dindex:
                sim_score = sims[other_id]
                if (sim_score >= thresholds[0] and  sim_score < thresholds[1] and id != other_id):
                    if (id < other_id):
                        first_id, second_id = id, other_id
                    else:
                        first_id, second_id = other_id, id
                    articles_and_sim[(first_id, second_id)] = sim_score
        return articles_and_sim



