import abc
from datetime import date, timedelta

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


    def find_related_articles(self, url,  max=15):
        record = self.article_loader.article_map[url]
        article = record["text"]
        date_record = record["date_p"]

        batch1 = self.get_related_articles_in_interval(article, date_record, 4000, 5, 15)
        batch2 = self.get_related_articles_in_interval(article, date_record, 2000, 10, 15)
        batch3 = self.get_related_articles_in_interval(article, date_record, 1000, 15, 15)
        return (batch1 + batch2 + batch3)[:max]

    @abc.abstractmethod
    def interesting_articles_for_day(self, start, end, max=15):
        pass
