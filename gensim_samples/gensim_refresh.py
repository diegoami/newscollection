import json
from os.path import basename
import argparse

from gensim import corpora, models, similarities
import logging

import sys
sys.path.append('..')
from gensim_samples.gensim_classifier import GensimClassifier
from gensim_samples.gensim_loader import GensimLoader

from gensim_samples.doc2vec_classifier import Doc2VecClassifier

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from datetime import datetime

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
#    argparser.add_argument('--fileName')
    argparser.add_argument('--dirName')
    argparser.add_argument('--listName')

    args = argparser.parse_args()
    gensimLoader = GensimLoader()

    if (args.dirName):
        gensimLoader.load_articles_from_directory(dirname = args.dirName, listname=args.listName, load_texts=True)

    gensim_root_filename = 'models/lsi/artmodel_'+ datetime.now().isoformat()
    gensimClassifier = GensimClassifier(dict_filename=gensim_root_filename + '.dict',
                corpus_filename=gensim_root_filename + '.mm', lsi_filename=gensim_root_filename + '.lsi', index_filename=gensim_root_filename + '.index')
    gensimClassifier.update_models(gensimLoader.articles)

  #  doc2vec_root_filename = 'models/doc2vec/doc2vecmodel_' + datetime.now().isoformat()
#    doc2vecClassifier = Doc2VecClassifier(dict_filename=doc2vec_root_filename + '.model')
 #   doc2vecClassifier.update_models(gensimLoader.articles, gensimLoader.urls)





