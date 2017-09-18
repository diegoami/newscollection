import json
from os.path import basename
import argparse

from gensim import corpora, models, similarities
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def load_stuff(fileName):
    articles, titles, texts, urls = [], [], [], []
    with open(fileName) as f:
        jsload = json.load(f)
        posts = jsload
        if "posts" in jsload:
            posts = jsload["posts"]
        for post in jsload["posts"]:
            title = post["title"]
            text = post["text"]
            url = post["url"]
            articles.append(title + '\n' + text)
            titles.append(title)
            texts.append(text)
            urls.append(url)
    return titles, texts, articles, urls

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--fileName')

    args = argparser.parse_args()
    titles, texts, documents, urls = load_stuff(args.fileName)
    
    
    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
          for document in documents]

    # remove words that appear only once
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
     for token in text:
         frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
          for text in texts]

    from     pprint import pprint  # pretty-printer


    dictionary = corpora.Dictionary(texts)
    dictionary.save(basename(args.fileName)+'.dict') # store the dictionary, for future reference
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(basename(args.fileName) + '.mm', corpus)

