MIN_FREQUENCY = 3
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'
TFIDF_FILENAME        = 'tfidf'


from datetime import timedelta, date

import numpy as np
import pandas as pd
from gensim import corpora, models, similarities
from gensim import matutils
from gensim.corpora import MmCorpus

from .tfidf_matrix_wrapper import TfidfMatrixWrapper
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer
from technews_nlp_aggregator.common.util import get_start_and_end




class TfidfFacade():

    def __init__(self, model_dir, article_loader=None, gramFacade=None, tokenizer=None, version=1):
        self.model_dir = model_dir
        self.article_loader = article_loader
        self.name = 'TFIDF-V'+str(version)
        self.gramFacade = gramFacade
        self.tokenizer = tokenizer


    def load_models(self):
        self.dictionary = corpora.Dictionary.load(self.model_dir + '/'+DICTIONARY_FILENAME)  # store the dictionary, for future reference
        self.corpus = MmCorpus(self.model_dir + '/'+ CORPUS_FILENAME )
        self.lsi = models.LsiModel.load(self.model_dir + '/'+ LSI_FILENAME)
        self.matrix_wrapper = TfidfMatrixWrapper(similarities.MatrixSimilarity.load(self.model_dir + '/'+ INDEX_FILENAME))  # transform corpus to LSI space and
        self.tfidf = models.TfidfModel.load(self.model_dir + '/'+ TFIDF_FILENAME)

    def get_vec(self, doc, title=''):
        tokenized_doc = self.get_tokenized(doc=doc, title=title)
        return self.get_vec_from_tokenized(tokenized_doc)

    def get_vec_from_tokenized(self, tokenized_doc):
        vec_bow = self.get_doc_bow(tokenized_doc)
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi


    def get_doc_bow(self, tokenized_doc):
        vec_bow = self.dictionary.doc2bow(tokenized_doc)
        return vec_bow

    def get_absent_words(self, tokenized_doc):
        abs_words = set([x for x in tokenized_doc if self.dictionary.dfs.get(x,0) == 0])
        return abs_words


    def get_tokenized(self, doc, title=''):
        words = self.tokenizer.tokenize_doc( doc=doc, title=title)
        p_words = self.gramFacade.phrase(words)
        return p_words

    def get_vec_docid(self, id):
        vec_bow = self.corpus[id]
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def docs_in_model(self):
        return self.corpus.num_docs

    def get_related_articles_and_score_doc(self, doc, start=None, end=None, title=''):
        articlesModelDF = self.article_loader.articlesDF.iloc[:self.corpus.num_docs]
        vec_lsi = self.get_vec(doc=doc, title=title)
        if (start and end):
            interval_condition = (articlesModelDF ['date_p'] >= start) & (articlesModelDF ['date_p'] <= end)
            scores = self.matrix_wrapper[(vec_lsi, interval_condition) ]
            articlesFilteredDF = articlesModelDF [interval_condition ]
        else:
            scores = self.matrix_wrapper[(vec_lsi,None)]
            articlesFilteredDF = articlesModelDF
        args_scores = np.argsort(-scores)
        new_index = articlesFilteredDF.iloc[args_scores].index
        df = pd.DataFrame(scores[args_scores], index=new_index, columns=['score'])
        return df


        #return articlesFilteredDF.iloc[args_scores].index, scores[args_scores]



    def get_score_id_id(self, id1, id2):

        vec_bow1 = self.corpus[id1]
        vec_lsi1 = self.lsi[vec_bow1]
        query1= matutils.unitvec(vec_lsi1 )
        query1 = np.array([x[1] for x in query1])

        vec_bow2 = self.corpus[id2]
        vec_lsi2 = self.lsi[vec_bow2]
        query2 = matutils.unitvec(vec_lsi2)
        query2 = np.array([x[1] for x in query2])

        return np.dot(query1, query2.T)

    def get_score_doc_doc(self, tok1, tok2):

        vec_doc1 = self.get_vec_from_tokenized(tok1)
        query1 = matutils.unitvec(vec_doc1 )
        query1 = np.array([x[1] for x in query1])

        vec_doc2 = self.get_vec_from_tokenized(tok2)
        query2 = matutils.unitvec(vec_doc2 )
        query2 = np.array([x[1] for x in query2])
        if (len(query1) == len(query2)):
            return np.dot(query1, query2.T)
        else:
            return 0


    def get_related_articles_for_ids(self, ids, start=date.min, end=date.max):
        articlesDF = self.article_loader.articlesDF.iloc[:self.corpus.num_docs]
        interval_condition = (articlesDF['date_p'] >= start) & (articlesDF['date_p'] <= end)
        articlesFilteredDF = articlesDF[interval_condition]
        vec_lsi_vec = [[x[1] for x in self.get_vec_docid(id)] for id in ids]
        np_vec_lsi_vec = np.array(vec_lsi_vec )
        query = matutils.unitvec(np_vec_lsi_vec)
        return query


    def get_related_articles_for_id(self, id, d_days):
        articlesDF = self.article_loader.articlesDF.iloc[:self.corpus.num_docs]
        url_date = articlesDF.iloc[id]['date_p']

        start, end = get_start_and_end(url_date, d_days)
        interval_condition = (articlesDF['date_p'] >= start) & (articlesDF['date_p'] <= end)
        articlesFilteredDF = articlesDF[interval_condition]
        vec_lsi = self.get_vec_docid(id)
        scores = self.matrix_wrapper[(vec_lsi, interval_condition)]
        args_scores = np.argsort(-scores)
        new_index = articlesFilteredDF.iloc[args_scores].index
        df = pd.DataFrame(scores[args_scores], index=new_index , columns=['score'])
        return df

