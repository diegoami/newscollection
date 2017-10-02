import sklearn


import nltk
import re
import numpy as np

if __name__ == "__main__":


    stopwords = nltk.corpus.stopwords.words('english')

    # load nltk's SnowballStemmer as variabled 'stemmer'
    from nltk.stem.snowball import SnowballStemmer

    stemmer = SnowballStemmer("english")

    num_clusters = 10
    def tokenize_and_stem(text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems


    def tokenize_only(text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        return filtered_tokens

    def first_try():
        hash_v = sklearn.externals.joblib.load('hash_v.pkl')
        hash_m = sklearn.externals.joblib.load('hash_m.pkl')
        titles = sklearn.externals.joblib.load('titles.pkl')
        urls = sklearn.externals.joblib.load('urls.pkl')

    def second_try():

        query = "IF YOU'RE LIKE most iPhone users, when you upgraded to the newest version of iOS, Apple automatically migrated your settings, apps, and text messages. While there are benefits to wiping your phone and starting over—c'mon, you don't really need all those apps—there's also the possibility that you might lose valuable info hidden within your text messages."

        tfidf_model = sklearn.externals.joblib.load('tfidf_model.pkl')
        lsi_model   = sklearn.externals.joblib.load('lsi_model.pkl')
        titles = sklearn.externals.joblib.load('titles.pkl')
        texts= sklearn.externals.joblib.load('texts.pkl')
        dictionary = sklearn.externals.joblib.load('dictionary.pkl')
        corpus = sklearn.externals.joblib.load('corpus.pkl')
        index_sparse = sklearn.externals.joblib.load('index_sparse.pkl')
        print(len(titles))
        print(len(texts))

        # vectorize the text into bag-of-words and tfidf
        query_bow = dictionary.doc2bow(tokenize_and_stem(query))
        query_tfidf = tfidf_model[query_bow]
        query_lsi = lsi_model[query_tfidf]
        print(query_lsi)

        index_sparse.num_best = None
        #print(index_sparse[query_tfidf])
        aff_list = index_sparse[query_tfidf]
        print(aff_list.shape)
        arg_sorted = list(np.argsort(aff_list))[::-1]
        stdic = {}
        for i, s in enumerate(arg_sorted):
            stdic[s] = titles[i]

        for i in range(len(arg_sorted)-1,len(arg_sorted)-21,-1 ):
            print(stdic[i])

    second_try()

