from datetime import date

from test_queries.test_bootstrap import *

end = date(2017, 9, 30)
start = date(2017, 9, 20)

intfvecs  = tfidfFacade.interesting_articles_for_day(start, end)

indocvecs = doc2VecFacade.interesting_articles_for_day(start, end)
print( " =========== TFIDF ================")

for intfvec, sumscore,urls_of_day in intfvecs:
    print(intfvec,sumscore)
    for url_of_day in urls_of_day:
        print("\t\t\t"+url_of_day)

print( " =========== INDOCVEC ================")

for intdocvec, sumscore,   urls_of_day in indocvecs:
    print(intdocvec, sumscore)
    for url_of_day in urls_of_day:
        print("\t\t\t"+url_of_day)
