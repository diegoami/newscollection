import time

from technews_nlp_aggregator.test_query.test_bootstrap import *

while True:
    random_article_url = articleLoader.get_random_article()
    print(" ============= ARTICLE ==================")
    print(random_article_url)

    print(" ============= DOC2VEC ==================")
    articles1 = doc2VecFacade.get_related_articles_and_score(random_article_url, 2000,30)
    print_articles(articles1)
    print(" ============= TFIDF==================")

    articles2 = tfidfFacade.get_related_articles_and_score(random_article_url, 2000,30 )
    print_articles(articles2)
    print(" ============= TOGETHER ==================")

    article_all = {}
    for article in articles1 + articles2:
        if article[0] in article_all:
            article_all[article[0]][2] += article[2]
    time.sleep(0.75)
