from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec

from technews_nlp_aggregator.nlp_model.common import Tokenizer

MODEL_FILENAME   = 'doc2vec'


import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
tokenizer = Tokenizer()

class LabeledLineSentence(object):
    def __init__(self, df):
        self.df = df
        self.labels_list = df['text'].tolist()
        self.titles_list = df['title'].tolist()
        self.doc_list = df.index.tolist()

    def __iter__(self):
        for idx, title, doc in zip(self.doc_list, self.titles_list, self.doc_list):
            wtok = tokenizer.tokenize_doc(title, doc)
            tags = [self.labels_list[idx]]

            yield TaggedDocument(words=wtok, tags=tags)

class Doc2VecGenerator:


    def __init__(self, articlesDF, model_output_dir):

        self.model_output_dir = model_output_dir
        self.articlesDF = articlesDF


    def create_model(self):

        it = LabeledLineSentence(self.articlesDF)

        self.model = Doc2Vec(size=300, window=10,  workers=11, alpha=0.025, min_alpha=0.025,
                             iter=10)  # use fixed learning rate
        self.model.build_vocab(it)

        logging.info("Starting to train......")

        # for epoch in range(10):
        #    logging.info("On epoch "+str(epoch))
        # model.train(it)
        # model.alpha -= 0.002 # decrease the learning rate
        # model.min_alpha = model.alpha # fix the learning rate, no deca
        self.model.train(it, total_examples=self.model.corpus_count, epochs=self.model.iter)
        #   logging.info("Finished training epoch " + str(epoch))

        logging.info("Training completed, saving to  " + self.model_output_dir)
        self.model.save(self.model_output_dir+MODEL_FILENAME )





