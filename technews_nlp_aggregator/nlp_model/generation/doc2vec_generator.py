from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec

from technews_nlp_aggregator.nlp_model.common import DefaultTokenizer

MODEL_FILENAME   = 'doc2vec'


import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class LabeledLineSentence(object):
    def __init__(self, texts, idxlist):
        self.texts = texts
        self.doc_list = idxlist

    def __iter__(self):
        for idx, text in zip(self.doc_list, self.texts):
            wtok = text
            tags = [idx]

            yield TaggedDocument(words=wtok, tags=tags)

class Doc2VecGenerator:


    def __init__(self, articlesDF, model_output_dir, tokenizer=None):

        self.model_output_dir = model_output_dir
        self.articlesDF = articlesDF
        self.tokenizer = DefaultTokenizer() if not tokenizer else tokenizer

    def create_model(self):
        texts = self.tokenizer.tokenize_ddf(self.articlesDF)
        it = LabeledLineSentence(texts, self.articlesDF.index )

        self.model = Doc2Vec(size=500, window=10,  workers=11, alpha=0.025, min_alpha=0.025,
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





