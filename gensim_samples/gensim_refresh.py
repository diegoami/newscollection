import json
from os.path import basename
import argparse

from gensim import corpora, models, similarities
import logging

import sys
sys.path.append('..')
from gensim_samples.gensim_lib import GensimClassifier

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--fileName')
    args = argparser.parse_args()
    base = basename(args.fileName)
    gensimClassifier = GensimClassifier(article_filename=args.fileName,  dict_filename=args.fileName + '.dict',
                corpus_filename=args.fileName + '.mm', lsi_filename=args.fileName + '.lsi', index_filename=args.fileName + '.index')
    gensimClassifier.update_models()
