from gensim.models import Word2Vec
from nltk.corpus import brown, movie_reviews, treebank, PlaintextCorpusReader
from six import string_types
from nltk.corpus.reader.util import concat



from datetime import datetime

wv = Word2Vec.load('/home/diego/qdata/techarticles/models/word2vec/model_2017-09-27T23:45:32.621447.model')
while True:
    st = input('--> ')
    print(wv.score(st))
