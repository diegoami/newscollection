import time

from tests.bootstrap.test_bootstrap import *

#while True:
#random_article_id, random_article = articleLoader.get_random_article()
random_article_id = 15073
random_article = articleLoader.articlesDF.loc[random_article_id]
# print(random_article)
print(" ============= ARTICLE ==================")
print(random_article["title"])

#print(" ============= DOC2VEC ==================")
#articles1 = doc2VecFacade.get_related_articles_and_score_docid(random_article_id , 2000,30)
#print(articles1)
print(" ============= TFIDF==================")

articles2 = tfidfFacade.get_related_articles_and_score_docid(random_article_id , 15,10 )
print(list(articles2["title"]))
print(list(articles2["text"]))

print(articles2)
print(" ============= TOGETHER ==================")

#  article_all = {}
#   for article in articles1 + articles2:
#       if article[0] in article_all:
#           article_all[article[0]][2] += article[2]
time.sleep(0.75)
