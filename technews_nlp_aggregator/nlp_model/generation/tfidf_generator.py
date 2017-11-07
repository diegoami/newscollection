
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'

from gensim import corpora, models, similarities

from technews_nlp_aggregator.nlp_model.common import DefaultTokenizer

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class TfidfGenerator:


    def __init__(self, model_output_dir):

        self.model_output_dir = model_output_dir

    def create_model(self, texts):

        dictionary = corpora.Dictionary(texts)
        logging.info("Initializing dictionary with {} texts".format(len(texts)))

        dictionary.filter_extremes(no_below=5, no_above=0.78, keep_n=150000)
        dictionary.save(self.model_output_dir+DICTIONARY_FILENAME)  # store the dictionary, for future reference
        corpus = [dictionary.doc2bow(text) for text in texts]
        logging.info("Created {} bags of words".format(len(corpus)))

        corpora.MmCorpus.serialize(self.model_output_dir+CORPUS_FILENAME, corpus)
        tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
        logging.info("Tfidf initialized with {} docs ".format(tfidf.num_docs))

        corpus_tfidf = tfidf[corpus]
        lsi = models.LsiModel(corpus_tfidf, num_topics=500, id2word=dictionary, chunksize=50000)  # initialize an LSI transformation
        corpus_lsi = lsi[corpus_tfidf]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

        lsi.save(self.model_output_dir+LSI_FILENAME)  # same for tfidf, lda, ...

        index = similarities.MatrixSimilarity(lsi[corpus])  # transform corpus to LSI space and index it
        logging.info("Similarity Matrix Length : {} ".format(len(index)))

        index.save(self.model_output_dir+INDEX_FILENAME)





