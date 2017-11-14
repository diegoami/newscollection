import operator
class Doc2VecInfo():
    def __init__(self, model, facade):
        self.model = model
        self.facade = facade


    def get_vector_for_docid(self, docid):
        doclist = self.model.docvecs.doctag_syn0[docid].tolist()
        doczip = zip(range(len(doclist)),  doclist)
        docsorted = sorted(doczip,key=lambda x: abs(x[1]), reverse=True)
        return docsorted

    def get_vector_for_doc(self, doc, title):
        doclist = self.facade.get_vector(title=title, doc=doc)
        doczip = zip(range(len(doclist)), doclist)
        docsorted = sorted(doczip, key=lambda x: abs(x[1]), reverse=True)
        return docsorted
