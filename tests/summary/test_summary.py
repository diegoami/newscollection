import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


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
        summary_sentences = _.summaryFacade.summarize(title, text, random_article_id)
        print(title)
        for entry in summary_sentences:
            print(entry["sentence"])

if __name__ == '__main__':
    config = yaml.safe_load(open('../../config.yml'))
    application = Application(config, True)
    try_summarize(application)
