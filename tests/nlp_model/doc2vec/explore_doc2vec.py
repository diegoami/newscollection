import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import yaml
from technews_nlp_aggregator.application import Application

def test_compare_docs_to_id(application, n_articles=20):
    _ = application
    for i in range(n_articles):
        random_article_id, random_article=  _.articleLoader.get_random_article()
        print(" ============= ARTICLE ==================")
        print(random_article['text'])
        print(" ============= DOC2VEC ==================")
        sentences_tokenizer = _.tokenizer.sentence_tokenizer
        for sentence in sentences_tokenizer.sent_tokenize(  random_article['text']):
            scores = _.doc2VecFacade.compare_docs_to_id(random_article['title'], sentence, random_article_id)
            print(sentence)
            print(scores)


if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    test_compare_docs_to_id(application )
