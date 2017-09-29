import json


from gensim import corpora, models, similarities

import os

from gensim.corpora import MmCorpus
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class GensimClassifier:

    def __init__(self, dict_filename, corpus_filename, lsi_filename, index_filename):
        self.dict_filename = dict_filename

        self.corpus_filename = corpus_filename
        self.lsi_filename = lsi_filename
        self.index_filename = index_filename


    def load_models(self):
        self.dictionary = corpora.Dictionary.load(self.dict_filename)  # store the dictionary, for future reference
        self.corpus = MmCorpus(self.corpus_filename)
        self.lsi = models.LsiModel.load(self.lsi_filename)
        self.index = similarities.MatrixSimilarity.load(self.index_filename)  # transform corpus to LSI space and index it

    def update_models(self, documents):
        # remove common words and tokenize

        texts = [[word for word in document.lower().split()]
                 for document in documents]

        # remove words that appear only once
        from collections import defaultdict
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        texts = [[token for token in text if frequency[token] > 1]
                 for text in texts]



        dictionary = corpora.Dictionary(texts)
        dictionary.save(self.dict_filename)  # store the dictionary, for future reference
        corpus = [dictionary.doc2bow(text) for text in texts]
        corpora.MmCorpus.serialize(self.corpus_filename, corpus)

        tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
        corpus_tfidf = tfidf[corpus]
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary)  # initialize an LSI transformation
        corpus_lsi = lsi[corpus_tfidf]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

        lsi.save(self.lsi_filename)  # same for tfidf, lda, ...

        index = similarities.MatrixSimilarity(lsi[corpus])  # transform corpus to LSI space and index it
        index.save(self.index_filename)



    def get_vec(self,doc):
        vec_bow = self.dictionary.doc2bow(doc.lower().split())
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def get_related_articles(self, doc, n):
        vec_lsi = self.get_vec(doc)
        sims = self.index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return sims

    def do_print_related(self, doc):
        logging.debug(" ============ BASE ARTICLE  ========================")
        logging.debug(doc)
        logging.debug(" ============ RELATED TITLES =======================")
        related_articles = self.get_related_articles(doc,10)
        for article in related_articles:
            logging.debug(article)


