MIN_FREQUENCY = 3
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'


from gensim import corpora, models, similarities
from . import ClfFacade
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class TfidfGenerator(ClfFacade):

    def __init__(self, model_dir, article_loader=None, gramFacade=None, tokenizer=None):
        self.model_dir = model_dir


    def create_dictionary(self, texts):
        dictionary = corpora.Dictionary(texts)
        logging.info("Initializing dictionary with {} texts".format(len(texts)))

        dictionary.filter_extremes(no_below=5, no_above=0.78, keep_n=150000)
        dictionary.save(self.model_dir+DICTIONARY_FILENAME)  # store the dictionary, for future reference
        corpus = [dictionary.doc2bow(text) for text in texts]
        logging.info("Created {} bags of words".format(len(corpus)))

        corpora.MmCorpus.serialize(self.model_dir+CORPUS_FILENAME, corpus)
        return corpus, dictionary

    def create_model(self, corpus, dictionary):

        tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
        logging.info("Tfidf initialized with {} docs ".format(tfidf.num_docs))

        corpus_tfidf = tfidf[corpus]
        lsi = models.LsiModel(corpus_tfidf, num_topics=500, id2word=dictionary, chunksize=50000)  # initialize an LSI transformation
        corpus_lsi = lsi[corpus_tfidf]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

        lsi.save(self.model_dir+'/'+LSI_FILENAME)  # same for tfidf, lda, ...
        return lsi

    def create_matrix(self, lsi, corpus):
        index = similarities.MatrixSimilarity(lsi[corpus])  # transform corpus to LSI space and index it
        logging.info("Similarity Matrix Length : {} ".format(len(index)))

        index.save(self.model_dir+'/'+INDEX_FILENAME)


