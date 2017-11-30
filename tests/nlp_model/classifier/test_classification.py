import yaml

from technews_nlp_aggregator.application import Application


def retrieve_scores(application, n_articles=25):
    _ = application

    for i in range(n_articles):
        index, article = _.articleLoader.get_random_article()
        article_id = article['article_id']
        articles_similar = _.classifierAggregator.retrieve_articles_for_id(index, 3, 25, 0)
        first_five = articles_similar.iloc[:6]
        art_df = first_five.join(_.articleLoader.articlesDF)
        sources = art_df['source'].unique()
        if (len(sources) == 1):
            print(article['title'], sources[0])

        #print(sources)

if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    retrieve_scores(application)
