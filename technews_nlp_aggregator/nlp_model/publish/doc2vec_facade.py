from gensim.models import Doc2Vec

from technews_nlp_aggregator.nlp_model.publish.clf_facade import ClfFacade

from technews_nlp_aggregator.nlp_model.common import defaultTokenizer

MODEL_FILENAME = 'doc2vec'


import numpy as np
from gensim.models.doc2vec import TaggedDocument

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class LabeledLineSentence(object):
    def __init__(self, idxlist, texts):
        self.doc_list = idxlist
        self.texts = texts

    def __iter__(self):
        for idx, text in zip(self.doc_list, self.texts):
            wtok = text
            tags = [idx]

            yield TaggedDocument(words=wtok, tags=tags)


class Doc2VecFacade(ClfFacade):

    def __init__(self, model_dir, article_loader=None, gramFacade=None, tokenizer=None):

        self.model_dir = model_dir
        self.article_loader = article_loader
        self.name="DOC2VEC-V4-600"
        self.gramFacade = gramFacade
        self.tokenizer = defaultTokenizer if not tokenizer else tokenizer

    def load_models(self):
        model_filename = self.model_dir+'/'+MODEL_FILENAME
        self.model = Doc2Vec.load(model_filename)


    def get_related_articles_and_sims(self, doc, n):
        wtok = self.tokenizer.tokenize_doc('', doc)
        p_wtok = self.gramFacade.phrase(wtok)
        infer_vector = self.model.infer_vector(p_wtok )

        similar_documents = self.model.docvecs.most_similar([infer_vector], topn=n)

        return similar_documents




    def get_related_articles_and_sims_id(self, id, n):
        similar_documents = self.model.docvecs.most_similar([id], topn=n)

        return similar_documents


    def compare_sentences_to_id(self, sentences, id):
        condition = self.article_loader.articlesDF.index == id
        articlesFilteredDF = self.article_loader.articlesDF[condition]
        dindex = articlesFilteredDF.index
        indexer = DocVec2Indexer(self.model.docvecs, dindex)
        scores = []
        for sentence in sentences:
            wtok = self.tokenizer.tokenize_doc('', sentence)
            p_wtok = self.gramFacade.phrase(wtok)

            infer_vector = self.model.infer_vector(p_wtok)

            score = self.model.docvecs.most_similar([infer_vector], topn=None, indexer=indexer)
            scores.append(score[0])
        return np.array(scores)


    def compare_docs_to_id(self,title, doc, id):
        wtok = self.tokenizer.tokenize_doc(title, doc)
        p_wtok = self.gramFacade.phrase(wtok)
        condition = self.article_loader.articlesDF.index == id
        articlesFilteredDF = self.article_loader.articlesDF[condition]
        dindex = articlesFilteredDF.index
        infer_vector = self.model.infer_vector(p_wtok)
        scores = self.model.docvecs.most_similar([infer_vector], topn=None, indexer=DocVec2Indexer(self.model.docvecs, dindex))
        return scores

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





    def get_related_articles_and_score_url(self, url, d_days):
        #docrow = self.article_loader.articlesDF[self.article_loader.articlesDF['article_id'] == docid]

        url_condition = self.article_loader.articlesDF['url'] == url

        docrow = self.article_loader.articlesDF[url_condition]
        if (len(docrow) > 0):
            docid = docrow.index[0]
            url_date = docrow.iloc[0]['date_p']
            interval_condition = abs((self.article_loader.articlesDF['date_p'] - url_date).dt.days) <= d_days
            articlesFilteredDF = self.article_loader.articlesDF[interval_condition]
            dindex = articlesFilteredDF.index
            indexer = DocVec2Indexer(self.model.docvecs, dindex)

            scores = self.model.docvecs.most_similar([docid], topn=None, indexer=DocVec2Indexer(self.model.docvecs, dindex))

            args_scores = np.argsort(-scores)
            return articlesFilteredDF.iloc[args_scores].index, scores[args_scores]
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

    def create_model(self, texts):

        it = LabeledLineSentence(range(len(texts)), texts)
        logging.info("Creating model with {} texts".format(len(texts)))
        self.model = Doc2Vec(size=600, window=10, workers=11, alpha=0.05,
                             iter=30, min_count=5)  # use fixed learning rate
        self.model.build_vocab(it)

        logging.info("Starting to train......")

        self.model.train(it, total_examples=self.model.corpus_count, epochs=self.model.iter)

        logging.info("Training completed, saving to  " + self.model_dir)
        self.model.save(self.model_dir + MODEL_FILENAME)


class DocVec2Indexer():
    def __init__(self, doc2vec, dindex):
        self.doc2vec = doc2vec

        self.dindex = dindex



    def most_similar(self, mean, topn):
        dists = np.dot(self.doc2vec.doctag_syn0norm[self.dindex], mean)
        return dists
