MIN_FREQUENCY = 3
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'


from gensim import corpora, models, similarities
from gensim.corpora import MmCorpus

from .tfidf_matrix_wrapper import TfidfMatrixWrapper
import numpy as np
from gensim import matutils
import pandas as pd
from pandas import DataFrame
from datetime import timedelta


class TfidfFacade():

    def __init__(self, model_dir, article_loader=None, gramFacade=None, tokenizer=None):
        self.model_dir = model_dir
        self.article_loader = article_loader
        self.name = 'TFIDF-V4-500'
        self.gramFacade = gramFacade
        self.tokenizer = tokenizer

    def load_models(self):
        self.dictionary = corpora.Dictionary.load(self.model_dir + '/'+DICTIONARY_FILENAME)  # store the dictionary, for future reference
        self.corpus = MmCorpus(self.model_dir + '/'+ CORPUS_FILENAME )
        self.lsi = models.LsiModel.load(self.model_dir + '/'+ LSI_FILENAME)
        self.matrix_wrapper = TfidfMatrixWrapper(similarities.MatrixSimilarity.load(self.model_dir + '/'+ INDEX_FILENAME))  # transform corpus to LSI space and

    def get_vec(self, doc, title=''):
        vec_bow = self.get_doc_bow(doc=doc, title=title)
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def get_doc_bow(self, doc, title=''):
        p_words = self.get_tokenized(doc=doc, title=title)
        vec_bow = self.dictionary.doc2bow(p_words)
        return vec_bow

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

    def get_score_doc_doc(self, doc1, doc2):

        vec_doc1 = self.get_vec(doc1)
        query1 = matutils.unitvec(vec_doc1 )
        query1 = np.array([x[1] for x in query1])

        vec_doc2 = self.get_vec(doc2)
        query2 = matutils.unitvec(vec_doc2 )
        query2 = np.array([x[1] for x in query2])

        return np.dot(query1, query2.T)



    def get_related_articles_for_id(self, id, d_days):
        articlesDF = self.article_loader.articlesDF.iloc[:self.corpus.num_docs]
        url_date = articlesDF.iloc[id]['date_p']
        start, end = url_date - timedelta(d_days) , url_date + timedelta(d_days)
        interval_condition = (articlesDF['date_p'] >= start) & (articlesDF['date_p'] <= end)
        articlesFilteredDF = articlesDF[interval_condition]
        vec_lsi = self.get_vec_docid(id)
        scores = self.matrix_wrapper[(vec_lsi, interval_condition)]
        args_scores = np.argsort(-scores)
        new_index = articlesFilteredDF.iloc[args_scores].index
        df = pd.DataFrame(scores[args_scores], index=new_index , columns=['score'])
        return df

