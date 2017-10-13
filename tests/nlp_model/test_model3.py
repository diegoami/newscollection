import time

from tests.bootstrap.test_bootstrap import *

while True:
    random_article = articleLoader.get_random_article()
    print(" ============= ARTICLE ==================")
    print(random_article)

    random_article_id = random_article['article_id']
    random_article_id_indx = random_article.index[0]
    print(" ============= DOC2VEC ==================")
    articles1 = doc2VecFacade.get_related_articles_and_docid(random_article_id , 2000,30)
    print_articles(articles1)
    print(" ============= TFIDF==================")

    articles2 = tfidfFacade.get_related_articles_and_docid(random_article_id , 2000,30 )
    print_articles(articles2)
    print(" ============= TOGETHER ==================")

  #  article_all = {}
 #   for article in articles1 + articles2:
 #       if article[0] in article_all:
 #           article_all[article[0]][2] += article[2]
    time.sleep(0.75)
