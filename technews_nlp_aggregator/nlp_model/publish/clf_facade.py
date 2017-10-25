import abc
from datetime import date, timedelta, datetime
import pandas as pd


class   ClfFacade:

    def __init__(self, model_filename, article_loader):
        self.model_filename = model_filename
        self.article_loader = article_loader





    def get_related_articles_in_interval(self, doc, reference_day=None, n=10000, days=5, max=15):


        if not reference_day:
            reference_day= date.today()
        start = reference_day - timedelta(days=days)
        end = reference_day + timedelta(days=days)

        return self.get_related_articles_from_to(doc, max, start, end, n )


    def find_related_articles(self, indx,  max=15):
        article = self.article_loader.articlesDF.loc[indx]
        article_text = article['text']
        date_p = article['date_p']

        batch1 = self.get_related_articles_in_interval(article_text, date_p, 4000, 5, 15)
        batch2 = self.get_related_articles_in_interval(article_text, date_p, 2000, 10, 15)
        batch3 = self.get_related_articles_in_interval(article_text, date_p, 1000, 15, 15)
        return pd.concat([batch1,batch2,batch3])

    def add_score_column(self, df_similar, refDay, we_score):

        if (refDay == None):
            refDay = datetime.datetime.now()
        tdelta = refDay - df_similar['date_p']
        tdays = tdelta .astype('timedelta64[D]')
        df_similar['score_total'] = df_similar['score'] * we_score - abs(tdays)
        return df_similar


    def enrich_with_score(self, similar_documents, we_score, refDay=None):
        id_articles, score_ids = zip(*similar_documents)


       # print(id_articles)
        df_similar = pd.DataFrame(self.article_loader.articlesDF.loc[id_articles, :])
       # print(df_similar[['title','article_id']])
        df_similar['score'] = list(score_ids)
        df_similar = self.add_score_column(df_similar, refDay, we_score)
        df_similar_ss = df_similar.sort_values(by='score_total', ascending=False)
        return df_similar_ss


