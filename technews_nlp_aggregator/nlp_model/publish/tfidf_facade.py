MIN_FREQUENCY = 3
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'

import logging

from gensim import corpora, models, similarities
from gensim.corpora import MmCorpus
from nltk.tokenize import word_tokenize

import pandas as pd

import datetime

from technews_nlp_aggregator.nlp_model.publish.clf_facade import ClfFacade

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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
        words = [word for word in word_tokenize(doc.lower())]
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
        return sims[1:n]


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
        docrow = self.article_loader.articlesDF[self.article_loader.articlesDF['article_id'] == docid]
        docidx = docrow.index[0]
        similar_documents = self.get_related_sims_docid(docidx , n)
        df_similar_docs = self.enrich_with_score(similar_documents,100)

        return df_similar_docs.iloc[:max,:]


    def get_related_articles_from_to(self, doc, max, start, end, n=10000):
        similar_documents = self.get_related_articles_and_score_doc(doc, n)
        id_articles, score_ids = zip(*similar_documents)
        articlesFilteredDF = self.article_loader.articlesDF.iloc[list(id_articles), :]

        articlesFoundDF = articlesFilteredDF[(articlesFilteredDF ['date_p'] >= start) & (articlesFilteredDF['date_p'] <= end)]
        #articlesFilteredDF.setIndex('article_id', drop=True)

        return articlesFoundDF

    def interesting_articles_for_day(self, start, end, max=15):
        docs_of_day = self.article_loader.docs_in_interval(start, end)
        all_links = []
        for docid in docs_of_day:
            ars_score = self.get_related_articles_and_score_docid(docid, 6000, 4)
            sum_score = sum([x[1] for x in ars_score])
            url = self.article_loader.url_list[docid]


            all_links.append((url, round(sum_score, 2), [x[0] for x in ars_score]))
        sall_links = sorted(all_links, key=lambda x: x[1], reverse=True)[:max]
        return sall_links