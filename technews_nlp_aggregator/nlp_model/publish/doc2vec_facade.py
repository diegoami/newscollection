from gensim.models import Doc2Vec
from nltk.tokenize import word_tokenize
import datetime
from technews_nlp_aggregator.nlp_model.publish.clf_facade import ClfFacade
import pandas as pd
from technews_nlp_aggregator.nlp_model.common import DefaultTokenizer

MIN_FREQUENCY = 3

from gensim import utils, matutils  # utility fnc for pickling, common scipy operations etc


from numpy import *
class Doc2VecFacade(ClfFacade):

    def __init__(self, model_filename, article_loader, tokenizer=None):
        self.model_filename = model_filename
        self.article_loader = article_loader
        self.name="DOC2VEC-V1-500"
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

    def get_related_articles(self, doc, n, days=None):
        similar_documents = self.get_related_articles_and_sims(doc,n)

        urls = list(zip(*similar_documents))[0]

        return urls

    def get_related_articles_and_score_doc(self, doc, n):

        return self.get_related_articles_and_sims(doc, n)




    def get_related_articles_and_score_url(self, url, n=10000, max=15 ):
        #docrow = self.article_loader.articlesDF[self.article_loader.articlesDF['article_id'] == docid]
        docrow = self.article_loader.articlesDF[self.article_loader.articlesDF['url'] == url]
        if (len(docrow) > 0):
            id = docrow.index[0]
            #id = self.article_loader.articlesDF.loc[docrow.index[0]]

            similar_documents = self.get_related_articles_and_sims_id(id, n)
            df_similar_docs = self.enrich_with_score(similar_documents, 200, docrow.iloc[0]["date_p"])
            return df_similar_docs.iloc[:max, :]
        else:
            return None

    def get_related_articles_and_score_docid(self, id, n=6000, max=15 ):
        #docrow = self.article_loader.articlesDF[self.article_loader.articlesDF['article_id'] == docid]
        docrow = self.article_loader.articlesDF.loc[id]

        similar_documents = self.get_related_articles_and_sims_id(id, n)
        df_similar_docs = self.enrich_with_score(similar_documents, 200, docrow ["date_p"])
        return df_similar_docs.iloc[:max, :]

    def compare_articles_from_dates(self,  start, end, thresholds):
        articles_and_sim = {}
        docs_of_day = self.article_loader.articles_in_interval(start, end)
        dindex = docs_of_day.index
        for id, row in docs_of_day.iterrows():
            dists = self.model.docvecs.most_similar([id], topn=15000, indexer=DocVec2Indexer(self.model.docvecs, id, dindex))
            for other_id, dist in zip(dindex, dists):
                if (dist >= thresholds[0] and  dist <= thresholds[1] and id != other_id):
                    if (id < other_id):
                        first_id, second_id = id, other_id
                    else:
                        first_id, second_id = other_id, id
                    articles_and_sim[(first_id, second_id)] = dist
        return articles_and_sim

class DocVec2Indexer():
    def __init__(self, doc2vec, id, dindex):
        self.doc2vec = doc2vec
        self.id = id
        self.dindex = dindex



    def most_similar(self, mean, topn):
        dists = dot(self.doc2vec.doctag_syn0norm[self.dindex], mean)
        return dists
