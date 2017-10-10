import time

from tests.bootstrap.test_bootstrap import *

while True:
    random_article_url = articleLoader.get_random_article()
    print(" ============= ARTICLE ==================")
    print(random_article_url)

    print(" ============= DOC2VEC ==================")
    articles1 = doc2VecFacade.find_related_articles(random_article_url)
    print_articles(articles1)
    print(" ============= TFIDF==================")

    articles2 = tfidfFacade.find_related_articles(random_article_url )
    print_articles(articles2)
    time.sleep(0.75)