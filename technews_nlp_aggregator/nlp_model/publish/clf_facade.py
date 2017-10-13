import abc
from datetime import date, timedelta, datetime
import pandas as pd


class ClfFacade:

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

        article_text = self.article_loader.articlesDF['text'].iloc[indx]
        date_p = self.article_loader.articlesDF['date_p'].iloc[indx]

        batch1 = self.get_related_articles_in_interval(article_text, date_p, 4000, 5, 15)
        batch2 = self.get_related_articles_in_interval(article_text, date_p, 2000, 10, 15)
        batch3 = self.get_related_articles_in_interval(article_text, date_p, 1000, 15, 15)
        return pd.concat([batch1,batch2,batch3])


    def enrich_with_score(self, similar_documents, we_score):
        id_articles, score_ids = zip(*similar_documents)
        df_similar = self.article_loader.articlesDF.iloc[id_articles, :]
        df_similar['score'] = pd.Series(score_ids)
        df_similar['from_today'] = datetime.datetime.now().date() - df_similar['p_date']
        df_similar['score_total'] = df_similar['score'] * we_score - df_similar['from_today']
        df_similar_ss = df_similar.sort_values(by='score_total', ascending=False)
        return df_similar_ss

    @abc.abstractmethod
    def interesting_articles_for_day(self, start, end, max=15):
        pass
