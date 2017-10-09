from gensim.models import Word2Vec
from nltk.corpus import brown, movie_reviews, treebank, PlaintextCorpusReader
from six import string_types
from nltk.corpus.reader.util import concat



from datetime import datetime

model = Word2Vec.load('/home/diego/qdata/techarticles/models/word2vec/model_2017-09-28T00:41:24.053958.model')
while True:
    st = input('--> ')
    if st in model.wv.vocab:
        print(model.score(st))
        print(model.most_similar(st))

    for s in st.split():
        if s in model.wv.vocab:

            print(model.most_similar(s))
