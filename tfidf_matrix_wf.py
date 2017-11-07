import logging
import os
import pickle
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.nlp_model.publish import TfidfGenerator
from datetime import datetime
import yaml
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
from gensim import corpora, models, similarities
from gensim import corpora, models, similarities
from gensim.corpora import MmCorpus

def create_tfidfmatrix(config):
    db_config = yaml.safe_load(open(config["key_file"]))
    model_dir = config["lsi_models_dir_link"]
    corpus = MmCorpus(model_dir + '/' + CORPUS_FILENAME)
    lsi = models.LsiModel.load(model_dir + '/' + LSI_FILENAME)
    tfidfGenerator = TfidfGenerator( model_dir)
    tfidfGenerator.create_matrix(lsi, corpus)


if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    create_tfidfmatrix(config)