import json
import argparse

import nltk
import re

import logging
import json

from itertools import chain
flatten = chain.from_iterable

from nltk import word_tokenize

from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models.tfidfmodel import TfidfModel



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

    tfidf = TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    n_topics = 10
    lda = models.LdaModel(corpus, num_topics=10,
                          id2word=dictionary,
                          update_every=10,
                          chunksize=10000,
                          passes=60)



    ## word lists
    for i in range(0, n_topics):
        temp = lda.show_topic(i, 10)
        terms = []
        for term in temp:
            terms.append(term)
        print("Top 10 terms for topic #" + str(i) + ": " + ", ".join([j[0] for j in terms]))

    from os import path
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud


    def terms_to_wordcounts(terms, multiplier=1000):
        return " ".join([" ".join(int(multiplier * j[1]) * [j[0]]) for j in terms])


    wordcloud = WordCloud(background_color="black").generate(terms_to_wordcounts(terms,100000   ))

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("terms1")

    plt.close()

    ## topic-words vectors: topics vs. words
    from sklearn.feature_extraction import DictVectorizer


    def topics_to_vectorspace(n_topics, n_words=100):
        rows = []
        for i in range(n_topics):
            temp = lda.show_topic(i, n_words)
            row = dict(((i[1], i[0]) for i in temp))
            rows.append(row)

        return rows


    vec = DictVectorizer()

    X = vec.fit_transform(topics_to_vectorspace(n_topics))
    X.shape
    # (40, 2457)

    ## PCA
    from sklearn.decomposition import PCA

    pca = PCA(n_components=2)

    X_pca = pca.fit(X.toarray()).transform(X.toarray())

    plt.figure()
    for i in range(X_pca.shape[0]):
        plt.scatter(X_pca[i, 0], X_pca[i, 1], alpha=.5)
        plt.text(X_pca[i, 0], X_pca[i, 1], s=' ' + str(i))

    plt.title('PCA Topics of Bart Strike Tweets')
    plt.savefig("pca_topic")

    plt.close()
