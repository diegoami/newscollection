import time

from tests.bootstrap.test_bootstrap import *

#while True:
random_article_id, random_article = articleLoader.get_random_article()
#random_article_id = 15073
random_article_url = random_article ['url']
# print(random_article)
print(" ============= ARTICLE ==================")
print(random_article["title"])

print(" ============= DOC2VEC ==================")
articles1, scores1 = doc2VecFacade.get_related_articles_and_score_url(random_article_url )
for idx, scr in zip(articles1[:100], scores1[:200] ):
    print(articleLoader.articlesDF.iloc[idx]['title'], scr)
print(" ============= TFIDF==================")

articles2, scores2 = tfidfFacade.get_related_articles_and_score_url(random_article_url  )
for idx, scr in  zip(articles2[:100], scores2[:200] ):
    print(articleLoader.articlesDF.iloc[idx]['title'], scr)


