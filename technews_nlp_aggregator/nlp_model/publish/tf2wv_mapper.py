from gensim import matutils
import numpy as np
import pandas as pd
DOCS_NUMPY_ARRAY = 'docs_numpy_array'
import logging
from gensim.matutils import unitvec
from .doc2vec_facade import DocVec2Indexer

class Tf2WvMapper:
    def __init__(self, gram_facade, tfidf_facade, doc2vec_facade):

        self.gram_facade = gram_facade
        self.tfidf_facade = tfidf_facade
        self.doc2vec_facade = doc2vec_facade


    def remap(self):
        self.dictionary = self.tfidf_facade.dictionary

        self.tfidf = self.tfidf_facade.tfidf
        self.idfs = self.tfidf.idfs
        self.id2word = self.tfidf_facade.lsi.id2word
        self.wv = self.doc2vec_facade.model.wv


    def get_wv(self, word):
        return self.wv.word_vec(word)

    def get_idf(self, word):
        return self.idfs[self.self.dictionary.token2id[word]]


    def get_weighted_vector(self, trigrams):
        vec_bow = self.dictionary.doc2bow(trigrams)
        return self.get_vec_bow(vec_bow)

    def get_weighted_vector_id(self, doc_id):
        vec_bow = self.tfidf_facade.corpus[ doc_id]
        return self.get_vec_bow(vec_bow)

    def get_vec_bow(self, vec_bow):
        vec_sum = np.zeros((1,self.doc2vec_facade.vector_size))

        for token_id, token_count in vec_bow:
            idf = self.idfs[token_id]
            token = self.dictionary[token_id]
            try:

                vec = self.get_wv(token)
                vec_sum = vec_sum + (token_count * idf) * vec
          #      logging.info(
           #         "Processed token {} with tf frequency {} ".format(token, self.tfidf_facade.dictionary.dfs.get(
            #                                                                              token_id, 0)))

            except KeyError:
                logging.info("Ignoring token {} with tf frequency {} - not found in WV".format(token,
                               self.tfidf_facade.dictionary.dfs.get(token, 0) ))

                continue
        vec_norm = unitvec(vec_sum )
        return vec_norm

    def get_vec_list(self, vec_bow):

        vec_list = []

        for token_id, token_count in vec_bow:
            idf = self.idfs[token_id]
            token = self.dictionary[token_id]
            try:
                logging.info("Trying token {} ".format(token))
                vec = self.get_wv(token)
                vec_weight_tuple = (vec, idf * token_count)
                logging.info("Vec of token {} for {}".format(token, idf * token_count))

                if (idf > 0 ):
                    vec_list.append(vec_weight_tuple )
            except KeyError:
                logging.info("Ignoring token {} - not found in WV".format(token))
                continue
        return vec_list



    def get_weighted_list(self, trigrams):
        vec_bow = self.dictionary.doc2bow(trigrams)
        return self.get_vec_list(vec_bow)

    def get_score_id_id(self, id1, id2):
        docvec1 = self.get_weighted_vector_id(id1)
        docvec1 = matutils.unitvec(docvec1)
        docvec2 = self.get_weighted_vector_id(id2)
        docvec2 = matutils.unitvec(docvec2)

        return np.dot(docvec1, docvec2.T)[0][0]

    def get_score_doc_doc(self, tok1, tok2):

        docvec1 = self.get_weighted_vector(tok1)
        docvec1 = matutils.unitvec(docvec1)
        docvec2 = self.get_weighted_vector(tok2)

        docvec2 = matutils.unitvec(docvec2)
        if (len(docvec1) == len(docvec2)):
            return np.dot(docvec1, docvec2.T)[0][0]
        else:
            return 0

    def get_related_articles_and_score_doc(self, doc, title= '',  start=None, end=None):
        infer_vector = self.get_weighted_vector(title+'\n'+doc)
        articleModelDF = self.doc2vec_facade.article_loader.articlesDF.iloc[:self.doc2vec_facade.model.docvecs.doctag_syn0.shape[0]]
        if (start and end):
            interval_condition = (articleModelDF ['date_p'] >= start) & (articleModelDF ['date_p'] <= end)
            articlesFilteredDF = articleModelDF [interval_condition]
            dindex = articlesFilteredDF.index
            indexer = DocVec2Indexer(self.model.docvecs,dindex )
            scores = self.model.docvecs.most_similar([infer_vector], topn=None, indexer=indexer)

        else:
            scores = self.model.docvecs.most_similar([infer_vector], topn=None)
            articlesFilteredDF = articleModelDF
            dindex = articlesFilteredDF.index

        args_scores = np.argsort(-scores)
        new_index = articlesFilteredDF.iloc[args_scores].index
        df = pd.DataFrame(scores[args_scores], index=new_index, columns=['score'])
        return df