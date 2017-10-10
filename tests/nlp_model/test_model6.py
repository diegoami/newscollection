#print(tfidfFacade.index.index.shape)
#print(tfidfFacade.corpus.index.shape)
#print(tfidfFacade.corpus[0])

#print(articleLoader.url_list[12000])
#print(tfidfFacade.get_related_articles_docid(12000,15))

#print(articleLoader.url_list[13000])
#print(tfidfFacade.get_related_articles_docid(13000,15))

#print(tfidfFacade.get_related_articles_and_score_docid(0,20000,15))
#print(tfidfFacade.get_related_articles_and_score_docid(1,20000,15))

#print(tfidfFacade.interesting_articles_for_day(date(2017,9,20), date(2017,9,25),15))


#print(articleLoader.url_list[10000])
#print(articleLoader.url_list[12000])

#print(doc2VecFacade.get_related_articles_and_sims_url(articleLoader.url_list[10000],15))
#print(doc2VecFacade.get_related_articles_and_score_url(articleLoader.url_list[12000],max=15))


#print(articleLoader.url_list[1])
#print(doc2VecFacade.get_related_articles_and_sims_url(articleLoader.url_list[1],15))
#print(doc2VecFacade.get_related_articles_and_score_url(articleLoader.url_list[1],max=15))


#def interesting_articles_for_day(self, start, end, max=15):

#print(doc2VecFacade.interesting_articles_for_day(date(2017,9,20), date(2017,9,25),15))
