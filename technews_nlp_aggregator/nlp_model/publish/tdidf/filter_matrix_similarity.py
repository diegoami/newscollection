from gensim.similarities import MatrixSimilarity

import logging
import itertools

from gensim import utils, matutils

class FilterMatrixSimilarity(MatrixSimilarity):
    def __init__(self, matrix):
        self.num_features = matrix.num_features
        self.num_best = matrix.num_best
        self.normalize = matrix.normalize
        self.chunksize = matrix.chunksize
        self.index = matrix.index

    def __getitem__(self, query):
        """Get similarities of document `query` to all documents in the corpus.

        **or**

        If `query` is a corpus (iterable of documents), return a matrix of similarities
        of all query documents vs. all corpus document. Using this type of batch
        query is more efficient than computing the similarities one document after
        another.
        """
        is_corpus, query = utils.is_corpus(query)
        if self.normalize:
            # self.normalize only works if the input is a plain gensim vector/corpus (as
            # advertised in the doc). in fact, input can be a numpy or scipy.sparse matrix
            # as well, but in that case assume tricks are happening and don't normalize
            # anything (self.normalize has no effect).
            if matutils.ismatrix(query):
                import warnings
                # warnings.warn("non-gensim input must already come normalized")
            else:
                if is_corpus:
                    query = [matutils.unitvec(v) for v in query]
                else:
                    query = matutils.unitvec(query)
        result = self.get_similarities(query)

        if self.num_best is None:
            return result

        # if maintain_sparity is True, result is scipy sparse. Sort, clip the
        # topn and return as a scipy sparse matrix.
        if getattr(self, 'maintain_sparsity', False):
            return matutils.scipy2scipy_clipped(result, self.num_best)

        # if the input query was a corpus (=more documents), compute the top-n
        # most similar for each document in turn
        if matutils.ismatrix(result):
            return [matutils.full2sparse_clipped(v, self.num_best) for v in result]
        else:
            # otherwise, return top-n of the single input document
            return matutils.full2sparse_clipped(result, self.num_best)




