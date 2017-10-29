
class Doc2VecInfo():
    def __init__(self, model):
        self.model = model


    def get_vector_for_docid(self, docid):
        return self.model.docvecs.doctag_syn0[docid]
