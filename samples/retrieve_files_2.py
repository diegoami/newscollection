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
        tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                           min_df=0.2, stop_words='english',
                                           use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3))


        tfidf_matrix = tfidf_vectorizer.fit_transform(texts)  # fit the vectorizer to synopses

        print(tfidf_matrix.shape)
        terms = tfidf_vectorizer.get_feature_names()


        dist = 1 - cosine_similarity(tfidf_matrix)

        hashing_vectorizer = HashingVectorizer(max_df=0.8, max_features=200000,
                                           min_df=0.2, stop_words='english',
                                           use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3))
        hashing_matrix = hashing_vectorizer.fit_transform(texts)  # fit the vectorizer to synopses


        sklearn.externals.joblib.dump(tfidf_matrix , 'tfidf.pkl')


        km = KMeans(n_clusters=num_clusters)

        km.fit(tfidf_matrix)


        clusters = km.labels_.tolist()

        return km, clusters, vocab_frame, terms, dist




    titles, texts, urls = load_stuff(args.fileName)
    km, clusters, vocab_frame, terms, dist = retr_model(titles,texts)
    clusters = km.labels_.tolist()
    df_texts= {'title': titles, 'texts': texts, 'cluster': clusters }
    oframe = pd.DataFrame(df_texts, columns=['cluster','title', 'texts']).reset_index()
    oframe[['cluster','title']].to_csv('clusters_g.csv')
    frame = oframe.groupby('cluster').count().reset_index()


    print("Top terms per cluster:")
    print()
    # sort cluster centers by proximity to centroid
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    wclusters = []
    for i in range(num_clusters):
        print("Cluster %d words:" % i, end='')
        ccluster = ""
        for ind in order_centroids[i, :10]:  # replace 6 with n words per cluster

            crc = vocab_frame.ix[terms[ind].split()].values.tolist()[0][0].encode('utf-8', 'ignore')
            ccluster = ccluster + " "+ str(crc)

            print(' %s' % crc,
                  end=',')
        wclusters.append(ccluster[:15])
        print()  # add whitespace
        print()  # add whitespace

        print("Cluster %d titles:" % i, end='')
        for title in oframe[oframe['cluster'] == i]['title']:
            print(' %s,' % title, end='')
        print()  # add whitespace
        print()  # add whitespace

    print()
    print()

    import os  # for os.path.basename

    import matplotlib.pyplot as plt
    import matplotlib as mpl

    from sklearn.manifold import MDS

    MDS()

    # convert two components as we're plotting points in a two-dimensional plane
    # "precomputed" because we provide a distance matrix
    # we will also specify `random_state` so the plot is reproducible.
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

    xs, ys = pos[:, 0], pos[:, 1]
    print()

    # set up cluster names using a dict
    cluster_names = {i:wclusters[i] for i in range(10) }

    # create models frame that has the result of the MDS plus the cluster numbers and titles
    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles))

    # group by cluster
    groups = df.groupby('label')

    # set up plot
    fig, ax = plt.subplots(figsize=(17, 9))  # set size
    ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling

    # iterate through groups to layer the plot
    # note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
                label=cluster_names[name],
                mec='none')
        ax.set_aspect('auto')
        ax.tick_params( \
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom='off',  # ticks along the bottom edge are off
            top='off',  # ticks along the top edge are off
            labelbottom='off')
        ax.tick_params( \
            axis='y',  # changes apply to the y-axis
            which='both',  # both major and minor ticks are affected
            left='off',  # ticks along the bottom edge are off
            top='off',  # ticks along the top edge are off
            labelleft='off')

    ax.legend(numpoints=1)  # show legend with only 1 point

    # add label in x,y position with the label as the film title
    for i in range(len(df)):
        ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)

    plt.show()  # show the plot

    from scipy.cluster.hierarchy import ward, dendrogram

    linkage_matrix = ward(dist)  # define the linkage_matrix using ward clustering pre-computed distances

    sklearn.externals.joblib.dump(dist, 'title_dist.pkl')
    sklearn.externals.joblib.dump(titles, 'titles.pkl')
    sklearn.externals.joblib.dump(urls, 'urls.pkl')

    fig, ax = plt.subplots(figsize=(30, 60))  # set size
    ax = dendrogram(linkage_matrix, orientation="right", labels=titles);

    plt.tick_params( \
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelbottom='off')

    plt.tight_layout()  # show plot with tight layout

    # uncomment below to save figure
    plt.savefig(basename(args.fileName)+'.png')  # save figure as ward_clusters

