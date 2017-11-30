import yaml

from technews_nlp_aggregator.application import Application
from technews_nlp_aggregator.nlp_model.spacy import spacy_nlp


def explore_lemmas(application, n_articles=20):
    _ = application

    for i in range(n_articles):
        index, article = _.articleLoader.get_random_article()
        article_id = article['article_id']
        article_with_text = _.articleDatasetRepo.load_article_with_text(article_id  )
        doc = spacy_nlp(article_with_text['ATX_TEXT'])
        lemmas = [(word.text, word.lemma_) for word in doc]
        print(lemmas)


if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    explore_lemmas(application)