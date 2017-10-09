from gensim.models import Word2Vec
from nltk.corpus import brown, movie_reviews, treebank, PlaintextCorpusReader
from six import string_types
from nltk.corpus.reader.util import concat




root_dir = '/home/diego/qdata/techarticles/parsed_articles/'
acr = PlaintextCorpusReader(root_dir, '.*\.txt')
#print(' ===================== PARAGRAPHS ================================')
#paras = acr.paras()
#print(' ===================== SENTENCES =================================')
#sents = acr.sents()

from datetime import datetime

b = Word2Vec(acr.sents())
b.save('/home/diego/qdata/techarticles/models/word2vec/model_'+ datetime.now().isoformat() +'.model')

'''
class ArticleCorpusReader(PlaintextCorpusReader):
    def raw(self, fileids=None):
        """
        :return: the given file(s) as a single string.
        :rtype: str
        """
        if fileids is None:
            fileids = self._fileids
        elif isinstance(fileids, string_types):
            fileids = [fileids]
        raw_texts = []
        for f in fileids:
            _fin = self.open(f)
            lines = _fin.readlines()
            article = "\n".join(lines[1:])
            raw_texts.append(article)
            _fin.close()
        return concat(raw_texts)

'''