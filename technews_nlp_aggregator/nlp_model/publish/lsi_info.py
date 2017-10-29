import numpy as np
import operator
from gensim import matutils
class LsiInfo():
    def __init__(self, model, corpus):
        self.model = model
        self.id2word = model.id2word
        self.num_topics = model.num_topics
        self.projection = model.projection
        self.corpus = corpus

    def get_topic_no_array(self, topicno):
        c = np.asarray(self.projection.u.T[topicno, :]).flatten()
        norm = np.sqrt(np.sum(np.dot(c, c)))
        most = matutils.argsort(np.abs(c))
        return [(self.id2word[val], 1.0 * c[val] / norm) for val in most]

    def get_words_docid(self, docid):
        vec = self.corpus[docid]
        wfreq = []
        for id, count in vec:
            word = self.id2word[id]
            wfreq.append((word, count))
        sfreq = sorted(wfreq, key=operator.itemgetter(1), reverse=True)
        return sfreq

    def get_topics_docid(self, docid):
        vec_bow = self.corpus[docid]
        vec_lsi = self.model[vec_bow]

        topic_freq = sorted([round(x,3) for x in vec_lsi] , key=lambda x: abs(x[1]), reverse=True)
        return topic_freq