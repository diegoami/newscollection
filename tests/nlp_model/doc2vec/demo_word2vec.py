import logging

import yaml
from technews_nlp_aggregator.application import Application


def word2vec_similar(application=None):
    _ = Application(config) if not application else application
    model = _.doc2VecFacade.model
    while True:
        st = input('--> ').lower()
        if st in model.wv.vocab:
            print(model.most_similar(st))

        for s in st.split():
            if s in model.wv.vocab:
                print(model.most_similar(s))

def word2vec_similar_negative(config, application=None):
    _ = Application(config) if not application else application
    model = _.doc2VecFacade.model
    while True:
        st = input('--> ').lower()
        pos, neg = st.split(',')
        posl, negl = pos.split(), neg.split()
        print(posl, negl)
        print(model.most_similar(positive=posl, negative=negl))



if __name__ == '__main__':
    config = yaml.safe_load(open('../../../computerconfig.yml'))
    application = Application(config, True)
    word2vec_similar(application )
