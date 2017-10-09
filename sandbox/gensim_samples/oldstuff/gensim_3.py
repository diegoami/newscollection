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


def test_hci():
    doc = "Human computer interaction"
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_lsi = lsi[vec_bow]  # convert the query to LSI space
    print(vec_lsi)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--fileName')

    args = argparser.parse_args()
    titles, texts, documents = load_stuff(args.fileName)


    dictionary = corpora.Dictionary.load(basename(args.fileName) + '.dict')  # store the dictionary, for future reference
    corpus =  MmCorpus(basename(args.fileName) + '.mm')
    lsi = models.LsiModel.load(basename(args.fileName) + '.lsi')

    index = similarities.MatrixSimilarity(lsi[corpus])  # transform corpus to LSI space and index it
    index.save(basename(args.fileName) + '.index')