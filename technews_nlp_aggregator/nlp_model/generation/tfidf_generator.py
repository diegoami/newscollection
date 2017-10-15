
MIN_FREQUENCY = 1
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'

from gensim import corpora, models, similarities

from technews_nlp_aggregator.nlp_model.common import Tokenizer

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class TfidfGenerator:


    def __init__(self, articleDF, model_output_dir):

        self.model_output_dir = model_output_dir
        self.articleDF = articleDF
        self.tokenizer  = Tokenizer()

    def create_model(self):
        texts = self.tokenizer(self.articleDF)


        dictionary = corpora.Dictionary(texts)
        dictionary.save(self.model_output_dir+DICTIONARY_FILENAME)  # store the dictionary, for future reference
        corpus = [dictionary.doc2bow(text) for text in texts]
        corpora.MmCorpus.serialize(self.model_output_dir+CORPUS_FILENAME, corpus)

        tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
        corpus_tfidf = tfidf[corpus]
        lsi = models.LsiModel(corpus_tfidf, id2word=dictionary)  # initialize an LSI transformation
        corpus_lsi = lsi[corpus_tfidf]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

        lsi.save(self.model_output_dir+LSI_FILENAME)  # same for tfidf, lda, ...

        index = similarities.MatrixSimilarity(lsi[corpus])  # transform corpus to LSI space and index it
        index.save(self.model_output_dir+INDEX_FILENAME)





