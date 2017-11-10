import logging
import os
import pickle

from technews_nlp_aggregator.nlp_model.publish import TfidfGenerator
from datetime import datetime
import yaml
from gensim import corpora, models, similarities
from gensim import corpora, models, similarities
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'

from gensim.corpora import MmCorpus
def create_tfidf_model(config):
    db_config = yaml.safe_load(open(config["key_file"]))
    model_dir = config["lsi_models_dir_link"]
    corpus = MmCorpus(model_dir + '/' + CORPUS_FILENAME)
    dictionary =  corpora.Dictionary.load(model_dir + '/'+DICTIONARY_FILENAME)  # store the dictionary, for future reference
    tfidfGenerator = TfidfGenerator( model_dir)
    lsi = tfidfGenerator.create_model(corpus, dictionary)





if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    create_tfidf_model(config)