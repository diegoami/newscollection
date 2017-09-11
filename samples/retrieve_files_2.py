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
        with open(fileName) as f:
            jsload = json.load(f)
            for post in jsload["posts"]:
                title = post["title"]
                text = post["text"]
                titles.append(title)
                texts.append(text)
        return titles, texts

    def retr_model(titles,texts):

        totalvocab_stemmed = []
        totalvocab_tokenized = []
        for text in texts:
            allwords_stemmed = tokenize_and_stem(text)  # for each item in 'synopses', tokenize/stem
            totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list

            allwords_tokenized = tokenize_only(text)
            totalvocab_tokenized.extend(allwords_tokenized)

        print(allwords_stemmed)
        print(allwords_tokenized)



        vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
        print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

        from sklearn.feature_extraction.text import TfidfVectorizer

        # define vectorizer parameters
        tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                           min_df=0.2, stop_words='english',
                                           use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3))


        tfidf_matrix = tfidf_vectorizer.fit_transform(texts)  # fit the vectorizer to synopses

        print(tfidf_matrix.shape)
        terms = tfidf_vectorizer.get_feature_names()


        dist = 1 - cosine_similarity(tfidf_matrix)




        km = KMeans(n_clusters=num_clusters)

        km.fit(tfidf_matrix)

        clusters = km.labels_.tolist()

        return km, clusters, vocab_frame, terms

    def save_stuff(km):


        joblib.dump(km,  'doc_cluster.pkl')


    titles, texts = load_stuff(args.fileName)
    if os.path.isfile('doc_cluster.pkl'):
        km = joblib.load('doc_cluster.pkl')
        km, clusters, vocab_frame, terms = retr_model(titles,texts)
        clusters = km.labels_.tolist()
        df_texts= {'title': titles, 'texts': texts, 'cluster': clusters }
        oframe = pd.DataFrame(df_texts, columns=['cluster','title', 'texts']).reset_index()
        oframe[['cluster','title']].to_csv('clusters_g.csv')
        frame = oframe.groupby('cluster').count().reset_index()
    else:
        save_stuff(titles, texts)


    print("Top terms per cluster:")
    print()
    # sort cluster centers by proximity to centroid
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]

    for i in range(num_clusters):
        print("Cluster %d words:" % i, end='')

        for ind in order_centroids[i, :6]:  # replace 6 with n words per cluster
            print(' %s' % vocab_frame.ix[terms[ind].split()].values.tolist()[0][0].encode('utf-8', 'ignore'),
                  end=',')
        print()  # add whitespace
        print()  # add whitespace

        print("Cluster %d titles:" % i, end='')
        for title in oframe[oframe['cluster'] == i]['title']:
            print(' %s,' % title, end='')
        print()  # add whitespace
        print()  # add whitespace

    print()
    print()