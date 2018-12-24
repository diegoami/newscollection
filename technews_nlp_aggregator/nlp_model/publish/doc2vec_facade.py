from gensim.models import Doc2Vec
from gensim import matutils


from technews_nlp_aggregator.nlp_model.common import defaultTokenizer
from technews_nlp_aggregator.common.util import get_start_and_end
MODEL_FILENAME = 'doc2vec'
import pandas as pd

import numpy as np
from gensim.models.doc2vec import TaggedDocument
from datetime import timedelta
import logging


class LabeledLineSentence(object):
    def __init__(self, idxlist, texts):
        self.doc_list = idxlist
        self.texts = texts

    def __iter__(self):
        for idx, text in zip(self.doc_list, self.texts):
            wtok = text
            tags = [idx]

            yield TaggedDocument(words=wtok, tags=tags)


class Doc2VecFacade():

    def __init__(self, model_dir, article_loader=None, gramFacade=None, tokenizer=None, window=10, min_count=5, sample=0.001, epochs=30, alpha=0.1, vector_size=400, batch_size=10000, queue_factor=2, workers=8, version=1):

        self.model_dir = model_dir
        self.article_loader = article_loader
        self.name="DOC2VEC-V"+str(version)
        self.gramFacade = gramFacade
        self.tokenizer = defaultTokenizer if not tokenizer else tokenizer
        self.window=window
        self.min_count=min_count
        self.sample = sample
        self.epochs = epochs
        self.alpha = alpha
        self.vector_size = vector_size
        self.batch_size = batch_size
        self.queue_factor = queue_factor
        self.workers = workers

    def load_models(self):
        model_filename = self.model_dir+'/'+MODEL_FILENAME
        self.model = Doc2Vec.load(model_filename)

    def get_vector(self, doc, title=''):
        tokenized_doc = self.get_tokenized(doc=doc, title=title)
        return self.get_vector_from_tokenized(tokenized_doc)


    def get_vector_from_tokenized(self, tokenized):
        infer_vector = self.model.infer_vector(tokenized, epochs=self.epochs, alpha=self.alpha)
        logging.info("DOC2VEC: infer_vector {} has shape {}".format(infer_vector, infer_vector.shape))
        return infer_vector



    def get_score_id_id(self, id1, id2):
        docvec1 = self.model.docvecs.doctag_syn0[id1]
        docvec1 = matutils.unitvec(docvec1)
        docvec2 = self.model.docvecs.doctag_syn0[id2]
        docvec2 = matutils.unitvec(docvec2)

        return np.dot(docvec1, docvec2.T)

    def get_score_doc_doc(self, tok1, tok2):

        docvec1 = self.get_vector_from_tokenized(tok1)
        docvec1 = matutils.unitvec(docvec1)
        docvec2 = self.get_vector_from_tokenized(tok2)

        docvec2 = matutils.unitvec(docvec2)
        if (len(docvec1) == len(docvec2)):
            return np.dot(docvec1, docvec2.T)
        else:
            return 0

    def get_tokenized(self, doc, title):
        wtok = self.tokenizer.tokenize_doc(title=title, doc=doc)
        p_wtok = self.gramFacade.phrase(wtok)
        return p_wtok

    def get_related_articles_and_score_doc(self, doc, title= '',  start=None, end=None):
        infer_vector = self.get_vector(doc, title)
        articleModelDF = self.article_loader.articlesDF.iloc[:self.model.docvecs.doctag_syn0.shape[0]]
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

    def get_related_articles_for_id(self, id, d_days):
        articleDF = self.article_loader.articlesDF.iloc[:self.model.docvecs.doctag_syn0.shape[0]]
        url_date = articleDF.iloc[id]['date_p']


        start, end = get_start_and_end(url_date, d_days)
        interval_condition = (articleDF['date_p'] >= start) & (articleDF['date_p'] <= end)

        articlesFilteredDF = articleDF[interval_condition]
        logging.info(
            "DOC2Vec: Found {} articles similar to {} between {} and {} ".format(len(articlesFilteredDF ), id, start, end))

        dindex = articlesFilteredDF.index
        indexer = DocVec2Indexer(self.model.docvecs, dindex)
        scores = self.model.docvecs.most_similar([id], topn=None, indexer=DocVec2Indexer(self.model.docvecs, dindex))
        args_scores = np.argsort(-scores)
        new_index = articlesFilteredDF.iloc[args_scores].index
        df = pd.DataFrame(scores[args_scores], index=new_index , columns=['score'])
        return df

    def create_model(self, texts):
        it = LabeledLineSentence(range(len(texts)), texts)
        logging.info("Creating model with {} texts".format(len(texts)))
        self.model = Doc2Vec(size=self.vector_size, window=self.window, workers=self.workers, alpha=self.alpha, min_alpha=0.0001,
                             epochs=self.epochs, min_count=self.min_count, sample=self.sample, batch_words=self.batch_size)  # use fixed learning rate
        self.model.build_vocab(it)

        logging.info("Starting to train......")

        self.model.train(it, total_examples=self.model.corpus_count, epochs=self.epochs, queue_factor=self.queue_factor)

        logging.info("Training completed, saving to  " + self.model_dir)
        self.model.save(self.model_dir + MODEL_FILENAME)

    def docs_in_model(self):
        return self.model.docvecs.doctag_syn0.shape[0]


class DocVec2Indexer():
    def __init__(self, doc2vec, dindex):
        self.doc2vec = doc2vec

        self.dindex = dindex



    def most_similar(self, mean, topn):
        dists = np.dot(self.doc2vec.doctag_syn0norm[self.dindex], mean)
        return dists
