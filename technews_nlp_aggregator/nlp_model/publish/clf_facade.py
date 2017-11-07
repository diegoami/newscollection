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




