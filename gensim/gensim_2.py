import json
from os.path import basename
import argparse

from gensim import corpora, models, similarities
import logging

from gensim.corpora import MmCorpus

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


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
            articles.append(title + '\n' + text)
            titles.append(title)
            texts.append(text)
    return titles, texts, articles


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--fileName')

    args = argparser.parse_args()
    titles, texts, documents = load_stuff(args.fileName)


    dictionary = corpora.Dictionary.load(basename(args.fileName) + '.dict')  # store the dictionary, for future reference
    corpus =  MmCorpus(basename(args.fileName) + '.mm')
    tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=20)  # initialize an LSI transformation
    corpus_lsi = lsi[corpus_tfidf]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
    lsi.print_topics(20)
    lsi.save(basename(args.fileName) + '.lsi')  # same for tfidf, lda, ...
