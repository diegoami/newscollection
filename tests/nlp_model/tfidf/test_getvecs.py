import yaml

from technews_nlp_aggregator.application import Application


def show_stuff(application, n_articles=10):
    _ = application
    for i in range(n_articles):
        index1, article1 = _.articleLoader.get_random_article()
        index2, article2 = _.articleLoader.get_random_article()
        vecdoc = _.tfidfFacade.get_related_articles_for_ids([index1, index2])
        print(vecdoc)

if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    show_stuff(application)

