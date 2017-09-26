import json
from os.path import basename
import argparse

from gensim import corpora, models, similarities
import logging

import sys
sys.path.append('..')
from gensim_samples.gensim_classifier import GensimClassifier
from gensim_samples.gensim_loader import GensimLoader
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from datetime import datetime

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--fileName')
    argparser.add_argument('--dirName')
    args = argparser.parse_args()
    gensimLoader = GensimLoader()
    if (args.fileName):
        gensimLoader.load_articles_from_json(article_filename=args.fileName)

    if (args.dirName):
        gensimLoader.load_articles_from_directory(dirname = args.dirName)

    root_filename = 'models/artmodel_'+ datetime.now().isoformat()
    gensimClassifier = GensimClassifier(dict_filename=root_filename  + '.dict',
                corpus_filename=root_filename  + '.mm', lsi_filename=root_filename + '.lsi', index_filename=root_filename + '.index')
    gensimClassifier.update_models(gensimLoader.articles)
