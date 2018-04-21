import yaml

from technews_nlp_aggregator.application import Application


def exact_search(application, n_articles=10):
    _ = application
    all_DF = _.articleLoader.articlesRepo.load_articles_containing('youtube shooting', 0, 25)
    print(all_DF)


if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    exact_search(application)

