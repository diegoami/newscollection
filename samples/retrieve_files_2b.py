import json
import argparse


import numpy as np
import pandas as pd
import nltk
import re
import sklearn
import os
import codecs
from sklearn import feature_extraction
from sklearn.externals import joblib
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from os.path import basename
from sklearn.metrics.pairwise import cosine_similarity

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
        titles = []
        texts = []
        #articles = []
        urls  = []
        with open(fileName) as f:
            jsload = json.load(f)
            posts = jsload
            if "posts" in jsload:
                posts = jsload["posts"]
            for post in posts:
                title = post["title"]
                text = post["text"]
                urls = post["url"]
                titles.append(title)
                texts.append(text)
                #articles.append(title+"\n"+ text)
        return titles, texts, urls

    def retr_model(titles,texts):

        totalvocab_stemmed = []
        totalvocab_tokenized = []
        for text in texts:
            try:
                allwords_stemmed = tokenize_and_stem(text)  # for each item in 'synopses', tokenize/stem
                totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list

                allwords_tokenized = tokenize_only(text)
                totalvocab_tokenized.extend(allwords_tokenized)
            except:
                print("Skipping text ... ")
        print(allwords_stemmed)
        print(allwords_tokenized)



        vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
        print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

        from sklearn.feature_extraction.text import TfidfVectorizer

        # define vectorizer parameters

        hashing_vectorizer = HashingVectorizer(
                                           stop_words='english',
                                           tokenizer=tokenize_and_stem, ngram_range=(1, 3))

        hashing_matrix = hashing_vectorizer .fit_transform(texts)  # fit the vectorizer to synopses




        sklearn.externals.joblib.dump(hashing_vectorizer , 'hash_v.pkl')

        sklearn.externals.joblib.dump(hashing_matrix , 'hash_m.pkl')


    titles, texts, urls = load_stuff(args.fileName)

    retr_model(titles, texts)
