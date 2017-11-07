
from technews_nlp_aggregator.application import Application
import yaml
import operator
from collections import defaultdict

def find_common_terms(application, n_terms=100):
    _ = application

    tokenized_docs = _.tokenizer.tokenize_ddf(_.articleLoader.articlesDF)

    frequency = defaultdict(int)
    for text in tokenized_docs:
        for token in text:
            frequency[token] += 1

    sorted_freq = sorted(frequency .items(), key=operator.itemgetter(1), reverse=True)
    sorted_keys = [x[0] for x in sorted_freq ]
    print(sorted_keys[:n_terms])

if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    find_common_terms(application )