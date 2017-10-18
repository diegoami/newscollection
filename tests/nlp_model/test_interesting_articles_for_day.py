from datetime import date

from tests.bootstrap.test_bootstrap import *

end = date(2017, 9, 21)
start = date(2017, 9, 20)

indocvecs = doc2VecFacade.interesting_articles_for_day(start, end)


print( " =========== INDOCVEC ================")


print(indocvecs)

intfvecs  = tfidfFacade.interesting_articles_for_day(start, end)
print( " =========== TFIDF ================")

print(intfvecs  )
