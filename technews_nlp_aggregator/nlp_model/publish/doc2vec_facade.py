from gensim.models import Doc2Vec
from nltk.tokenize import word_tokenize
import datetime
from technews_nlp_aggregator.nlp_model.publish.clf_facade import ClfFacade
import pandas as pd
from technews_nlp_aggregator.nlp_model.common import DefaultTokenizer
import numpy as np
MIN_FREQUENCY = 3

from gensim import utils, matutils  # utility fnc for pickling, common scipy operations etc


from numpy import *
class Doc2VecFacade(ClfFacade):

    def __init__(self, model_filename, article_loader, tokenizer=None):
        self.model_filename = model_filename
        self.article_loader = article_loader
        self.name="DOC2VEC-V3-600"
        self.tokenizer = DefaultTokenizer() if not tokenizer else tokenizer


    def load_models(self):
        self.model = Doc2Vec.load(self.model_filename)


    def get_related_articles_and_sims(self, doc, n):
        wtok = self.tokenizer.tokenize_doc('', doc)
        infer_vector = self.model.infer_vector(wtok)

        similar_documents = self.model.docvecs.most_similar([infer_vector], topn=n)

        return similar_documents




    def get_related_articles_and_sims_id(self, id, n):
        similar_documents = self.model.docvecs.most_similar([id], topn=n)

        return similar_documents



    def get_related_articles_and_score_doc(self, doc, start=None, end=None):
        wtok = self.tokenizer.tokenize_doc('', doc)
        infer_vector = self.model.infer_vector(wtok)

        if (start and end):
            interval_condition = (self.article_loader.articlesDF['date_p'] >= start) & (self.article_loader.articlesDF['date_p'] <= end)
            articlesFilteredDF = self.article_loader.articlesDF[interval_condition]
            dindex = articlesFilteredDF.index
            indexer = DocVec2Indexer(self.model.docvecs,dindex )
            scores = self.model.docvecs.most_similar([infer_vector], topn=None, indexer=indexer)

        else:
            scores = self.model.docvecs.most_similar([infer_vector], topn=None)
            articlesFilteredDF = self.article_loader.articlesDF
            dindex = articlesFilteredDF.index

        args_scores = np.argsort(-scores)
        return articlesFilteredDF.iloc[args_scores].index, scores[args_scores]





    def get_related_articles_and_score_url(self, url):
        #docrow = self.article_loader.articlesDF[self.article_loader.articlesDF['article_id'] == docid]

        url_condition = self.article_loader.articlesDF['url'] == url
        docrow = self.article_loader.articlesDF[url_condition]
        if (len(docrow) > 0):
            docid = docrow.index[0]
            scores = self.model.docvecs.most_similar([docid], topn=None)

            args_scores = np.argsort(-scores)
            return self.article_loader.articlesDF.iloc[args_scores].index, scores[args_scores]
        else:
            return None, None


    def compare_articles_from_dates(self,  start, end, thresholds):
        articles_and_sim = {}
        interval_condition = (self.article_loader.articlesDF['date_p'] >= start) & (self.article_loader.articlesDF['date_p'] <= end)
        articlesFilteredDF = self.article_loader.articlesDF[interval_condition]
        dindex = articlesFilteredDF.index
        for id in dindex:
            scores = self.model.docvecs.most_similar([id], topn=None, indexer=DocVec2Indexer(self.model.docvecs, dindex))

            scores_in_threshold_condition = (scores >= thresholds[0]) & (scores <= thresholds[1])
            scores_in_threshold = scores[scores_in_threshold_condition]
            id_in_threshold = articlesFilteredDF.index[scores_in_threshold_condition]

            articles_and_sim[id] = zip(id_in_threshold, scores_in_threshold)
        return articles_and_sim

class DocVec2Indexer():
    def __init__(self, doc2vec, dindex):
        self.doc2vec = doc2vec

        self.dindex = dindex



    def most_similar(self, mean, topn):
        dists = dot(self.doc2vec.doctag_syn0norm[self.dindex], mean)
        return dists
