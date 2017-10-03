from datetime import date

from technews_nlp_aggregator.test_query.test_bootstrap import *

end = date(2017, 9, 30)
start = date(2017, 9, 20)

intfvecs  = tfidfFacade.interesting_articles_for_day(start, end)

indocvecs = doc2VecFacade.interesting_articles_for_day(start, end)
print( " =========== TFIDF ================")

for intfvec, sumscore,str_score,urls_of_day in intfvecs:
    print(intfvec,sumscore,str_score)
    for url_of_day in urls_of_day:
        print("\t\t\t"+url_of_day)

print( " =========== INDOCVEC ================")

for intdocvec, sumscore, str_score,  urls_of_day in indocvecs:
    print(intdocvec, sumscore, str_score)
    for url_of_day in urls_of_day:
        print("\t\t\t"+url_of_day)
