import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import yaml

from technews_nlp_aggregator.application import Application


def show_tokens(application, n_articles=100):
    _ = application
    for i in range(n_articles):
        index, article = _.articleLoader.get_random_article()
        article_id = article['article_id']
        article_with_text = _.articleDatasetRepo.load_article_with_text(article_id  )
        tokens = _.tokenizeInfo.get_tokenized_article(article_with_text['AIN_TITLE'], article_with_text['ATX_TEXT'])
        trigrams = _.gramFacade.phrase(tokens)
        print(str(article_id )+' : ' +str(trigrams))




if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    show_tokens(application )