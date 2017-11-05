
from gensim.interfaces import utils, matutils
class TfidfMatrixWrapper():

    def __init__(self, similarityMatrix):
        self.similarityMatrix = similarityMatrix
        self.index = self.similarityMatrix.index[:]

    def __getitem__(self, tuple ):
        query, npdate = tuple

        simil_returned = self.similarityMatrix[query]

        if npdate is None:
            return simil_returned
        else:

            return simil_returned[npdate]

    def get_for_corpus(self, query, column):


        simil_returned = self.similarityMatrix[query]


        return simil_returned[:,column]
