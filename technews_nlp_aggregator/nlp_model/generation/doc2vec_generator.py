from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
import pickle
from technews_nlp_aggregator.nlp_model.common import DefaultTokenizer

MODEL_FILENAME   = 'doc2vec'


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

class Doc2VecGenerator:


    def __init__(self, model_output_dir):

        self.model_output_dir = model_output_dir


    def create_model(self, texts):

        self.it = LabeledLineSentence( range(len(texts)), texts)

        self.model = Doc2Vec(size=600, window=10,  workers=11, alpha=0.05,
                             iter=25, min_count=4, sample=0)  # use fixed learning rate
        self.model.build_vocab(self.it)

    def train_model(self):

        logging.info("Starting to train......")

        self.model.train(self.it, total_examples=self.model.corpus_count, epochs=self.model.iter)
        #   logging.info("Finished training epoch " + str(epoch))

        logging.info("Training completed, saving to  " + self.model_output_dir)
        self.model.save(self.model_output_dir+MODEL_FILENAME )





