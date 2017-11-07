

from technews_nlp_aggregator.application import Application
import yaml


def test_remove_sentences(application, n_articles=200):
    _ = application
    lastsentences_map = {}
    first_artDF = _.articlesDF.iloc[:n_articles,:]
    for index, row in first_artDF .iterrows():
        cleaned_text = _.word_tokenizer.sentenceTokenizer.clean_sentences(row['text'])
        print(cleaned_text)
        print()

if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    test_remove_sentences(application)