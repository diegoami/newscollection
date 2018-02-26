import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.publish import TfidfGenerator
import yaml
from gensim import corpora

DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'

from gensim.corpora import MmCorpus
def create_tfidf_model(config, param_config):
    db_config = yaml.safe_load(open(config["key_file"]))
    model_dir = config["root_dir"]+config["lsi_models_dir_link"]
    corpus = MmCorpus(model_dir + '/' + CORPUS_FILENAME)
    dictionary =  corpora.Dictionary.load(model_dir + '/'+DICTIONARY_FILENAME)  # store the dictionary, for future reference
    tfidfGenerator = TfidfGenerator( model_dir, no_below=int(param_config['tdf_no_below']), no_above=int(param_config['tdf_no_above']) , num_topics=int(param_config['tdf_num_topics']), version = config['version'] )
    lsi = tfidfGenerator.create_model(corpus, dictionary)

if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    version = config['version']
    param_config = yaml.safe_load(open('v_' + str(version) + '.yml'))
    create_tfidf_model(config, param_config)