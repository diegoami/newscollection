import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.WARN)

from technews_nlp_aggregator.application import Application
import yaml

def try_summarize(application, n_articles=20):
    _ = application
    for index in range(n_articles):

        random_article_id, random_article = _.articleLoader.get_random_article()
        random_article_url = random_article ['url']
        print(" ============= ARTICLE ==================")
        title, text = random_article["title"], random_article["text"]
        print(title)
        print(text)

        print(" ============= SUMMARY ==================")
        summary_sentences = _.summaryFacade.summarize(random_article_id,doc=text, title=title)
        print(title)
        for id, sent in summary_sentences:
            print("{} {}".format(id,sent))

def try_summarize_for_ana(application, n_articles=20):
    _ = application

    for index in range(n_articles):

        random_article_id, random_article = _.articleLoader.get_random_article()
        random_article_url = random_article ['url']
        print(" ============= ARTICLE ==================")
        title, text = random_article["title"], random_article["text"]
        print(title)
        print(text)

        print(" ============= SUMMARY 1 ==================")
        summary1 = _.summaryFacade.full_text_summarize(random_article_id, text, title, 0.85)
        print(summary1)

        print(" ============= SUMMARY 2 ==================")

        summary2 = _.summaryFacade.full_text_summarize(random_article_id, text, title, 0.7)
        print(summary2)

        print(" ============= EXCLUDED ==================")
        tok_doc = _.tfidfFacade.get_tokenized(text, title)

        abs_words_gf = _.gramFacade.words_not_in_vocab(tok_doc,100)
        abs_words_tf = _.tfidfFacade.get_absent_words(tok_doc)
        inters_words_tf = abs_words_gf.intersection(abs_words_tf )
        print(inters_words_tf )


if __name__ == '__main__':
    config = yaml.safe_load(open('../../config.yml'))
    application = Application(config, True)
    application.gramFacade.load_phrases()
    try_summarize_for_ana(application)


