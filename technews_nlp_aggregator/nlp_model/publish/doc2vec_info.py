import operator
class Doc2VecInfo():
    def __init__(self, model):
        self.model = model


    def get_vector_for_docid(self, docid):
        doclist = self.model.docvecs.doctag_syn0[docid].tolist()
        doczip = zip(range(len(doclist)),  doclist)
        docsorted = sorted(doczip,key=lambda x: abs(x[1]), reverse=True)
        return docsorted

