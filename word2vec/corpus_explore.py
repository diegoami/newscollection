
from gensim.models import Word2Vec
from nltk.corpus import brown, movie_reviews, treebank, PlaintextCorpusReader
from six import string_types
from nltk.corpus.reader.util import concat

root_dir = '/home/diego/qdata/techarticles/parsed_articles/'
acr = PlaintextCorpusReader(root_dir, '.*\.txt')
from datetime import datetime

print(acr.fileids())

for fileid in acr.fileids():
#    num_chars = len(acr.raw(fileid))
#    num_words = len(acr.words(fileid))
#    num_sents = len(acr.sents(fileid))
#    num_vocab = len(set(w.lower() for w in acr.words(fileid)))
#    print(round(num_chars / num_words), round(num_words / num_sents), round(num_words / num_vocab), fileid)
    print(" ============ "+fileid+ " =============================")
    print(acr.words(fileid ))
    print(acr.sents(fileid))
