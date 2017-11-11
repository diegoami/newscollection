import logging

from technews_nlp_aggregator.nlp_model.spacy import spacy_nlp
from technews_nlp_aggregator.application import Application

import yaml

def explore_user_paired(_):
    user_paired = _.articleSimilarLoader.retrieve_groups()
    return user_paired

if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    drows = explore_user_paired(application)
    print(drows)
