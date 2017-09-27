from gensim.models import Word2Vec
from nltk.corpus import brown, movie_reviews, treebank, PlaintextCorpusReader
from six import string_types
from nltk.corpus.reader.util import concat
import gensim



root_dir = '/home/diego/qdata/techarticles/parsed_articles/'
acr = PlaintextCorpusReader(root_dir, '.*\.txt')
#print(' ===================== PARAGRAPHS ================================')
#paras = acr.paras()
#print(' ===================== SENTENCES =================================')
sents = acr.sents()

from datetime import datetime



b = Word2Vec(acr.sents(), hs=1, negative=0)


b.save('/home/diego/qdata/techarticles/models/word2vec/model_'+ datetime.now().isoformat() +'.model')
