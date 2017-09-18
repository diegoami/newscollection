import json
import argparse


import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
from sklearn.externals import joblib
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models.tfidfmodel import TfidfModel
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--fileName')

    args = argparser.parse_args()

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


    # not super pythonic, no, not at all.
    # use extend so it's a big flat list of vocab
    def load_stuff(fileName):
        articles, titles, texts = [], [], []
        with open(fileName) as f:
            jsload = json.load(f)
            posts = jsload
            if "posts" in jsload:
                posts = jsload["posts"]
            for post in jsload["posts"]:
                title = post["title"]
                text = post["text"]
                articles.append(title +'\n' + text)
                titles.append(title)
                texts.append(text)
        return titles, texts, articles


    # strip any proper names from a text...unfortunately right now this is yanking the first word from a sentence too.
    import string




    def strip_proppers(text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent) if word.islower()]
        return "".join(
            [" " + i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()

    def do_print_titles(lis_model, dictionary, titles):
        for title in titles:
            print(title)
            doc = title
            vec_bow = dictionary.doc2bow(doc.lower().split())
            vec_lsi = lsi_model[vec_bow]  # convert the query to LSI space`
            print(vec_lsi)


    titles, texts, articles = load_stuff(args.fileName)

    # strip any proper nouns (NNP) or plural proper nouns (NNPS) from a text
    from nltk.tag import pos_tag


    def strip_proppers_POS(text):
        tagged = pos_tag(text.split())  # use NLTK's part of speech tagger
        non_propernouns = [word for word, pos in tagged if pos != 'NNP' and pos != 'NNPS']
        return non_propernouns


    from gensim import corpora, models, similarities

    preprocess = [strip_proppers(doc) for doc in articles]

    tokenized_text = [tokenize_and_stem(text) for text in preprocess]

    worked_texts = [[word for word in text if word not in stopwords] for text in tokenized_text]


    # create a Gensim dictionary from the texts
    dictionary = corpora.Dictionary(worked_texts )

    corpus = [dictionary.doc2bow(worked_text ) for worked_text in worked_texts]


    # convert the dictionary to a bag of words corpus for reference


    lsi_model = models.LsiModel(corpus, id2word=dictionary, num_topics=12)

    query = "April is the fourth month of the year, and comes between March \
        and May. It has 30 days. April begins on the same day of week as July in \
        all years and also January in leap years."

    query =  "IF YOU'RE LIKE most iPhone users, when you upgraded to the newest version of iOS, Apple automatically migrated your settings, apps, and text messages. While there are benefits to wiping your phone and starting over—c'mon, you don't really need all those apps—there's also the possibility that you might lose valuable info hidden within your text messages."

    tfidf_model = TfidfModel(corpus)
    corpus_tfidf = tfidf_model [corpus]
    from gensim.similarities import MatrixSimilarity, SparseMatrixSimilarity, Similarity

    index_sparse = SparseMatrixSimilarity(corpus, num_features=len(dictionary))

    import sklearn
    sklearn.externals.joblib.dump(tfidf_model , 'tfidf_model.pkl')
    sklearn.externals.joblib.dump(lsi_model, 'lsi_model.pkl')
    sklearn.externals.joblib.dump(texts, 'texts.pkl')

    sklearn.externals.joblib.dump(worked_texts, 'worked_texts.pkl')
    sklearn.externals.joblib.dump(titles, 'titles.pkl')
    sklearn.externals.joblib.dump(dictionary, 'dictionary.pkl')
    sklearn.externals.joblib.dump(corpus, 'corpus.pkl')
    sklearn.externals.joblib.dump(index_sparse, 'index_sparse.pkl')


