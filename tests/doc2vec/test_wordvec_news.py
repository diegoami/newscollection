from gensim.models import Doc2Vec, Word2Vec
model = Word2Vec()
model.wv.load_word2vec_format('/media/diego/QData/models/word2vec/GoogleNews-vectors-negative300.bin', binary=True)
while True:
    st = input('--> ').lower()
    pos, neg = st.split(',')
    posl, negl = pos.split(), neg.split()
    print(posl, negl)
    print(model.wv.most_similar(positive=posl, negative=negl))