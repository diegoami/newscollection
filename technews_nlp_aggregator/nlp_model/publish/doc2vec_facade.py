from gensim.models import Doc2Vec

from technews_nlp_aggregator.nlp_model.publish.clf_facade import ClfFacade

from technews_nlp_aggregator.nlp_model.common import defaultTokenizer
import numpy as np
MIN_FREQUENCY = 3


from numpy import *
import pandas as pd
class Doc2VecFacade(ClfFacade):

    def __init__(self, model_filename, article_loader, gramFacade, tokenizer=None):
        self.model_filename = model_filename
        self.article_loader = article_loader
        self.name="DOC2VEC-V4-600"
        self.gramFacade = gramFacade
        self.tokenizer = defaultTokenizer if not tokenizer else tokenizer


    def load_models(self):
        self.model = Doc2Vec.load(self.model_filename)


    def get_related_articles_and_sims(self, doc, n):
        wtok = self.tokenizer.tokenize_doc('', doc)
        p_wtok = self.gramFacade.phrase(wtok)
        infer_vector = self.model.infer_vector(p_wtok )

        similar_documents = self.model.docvecs.most_similar([infer_vector], topn=n)

        return similar_documents




    def get_related_articles_and_sims_id(self, id, n):
        similar_documents = self.model.docvecs.most_similar([id], topn=n)

        return similar_documents



    def get_related_articles_and_score_doc(self, doc, start=None, end=None):
        wtok = self.tokenizer.tokenize_doc('', doc)
        p_wtok = self.gramFacade.phrase(wtok)
        infer_vector = self.model.infer_vector(p_wtok)

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
            url_date = docrow.iloc[0]['date_p']
            scores = self.model.docvecs.most_similar([docid], topn=None)

            args_scores = np.argsort(-scores)
            return self.article_loader.articlesDF.loc[args_scores].index, scores[args_scores], abs(pd.to_numeric(self.article_loader.articlesDF['date_p'] - url_date))
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
