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

    texts = [[word for word in text if word not in stopwords] for text in tokenized_text]

    # create a Gensim dictionary from the texts
    dictionary = corpora.Dictionary(texts)

    # remove extremes (similar to the min/max df step used when creating the tf-idf matrix)
    dictionary.filter_extremes(no_below=1, no_above=0.8)

    # convert the dictionary to a bag of words corpus for reference
    corpus = [dictionary.doc2bow(text) for text in texts]

    lda = models.LdaModel(corpus, num_topics=10,
                          id2word=dictionary,
                          update_every=10,
                          chunksize=10000,
                          passes=60)

    lda.show_topics()

    topics_matrix = lda.show_topics(formatted=False, num_words=20)
    print(topics_matrix)

"""
    topic_words = topics_matrix[:, :, 1]
    for i in topic_words:
        print([str(word) for word in i])
        print()
"""
