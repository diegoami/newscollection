import abc
from datetime import date

class ClfFacade:

    def __init__(self, model_filename, article_loader):
        self.model_filename = model_filename
        self.article_loader = article_loader

    @abc.abstractmethod
    def load_models(self):
        pass

    @abc.abstractmethod
    def get_related_sims(self, doc, n):
        pass

    @abc.abstractmethod
    def get_related_articles(self, doc, n):
        pass

    @abc.abstractmethod
    def get_related_articles_and_score(self, doc, n):
        pass

    @abc.abstractmethod
    def get_related_articles_and_score(self, urlArg, n=5000, max=15):
        pass

    def get_related_articles_in_interval(self, doc, reference_day=None, n=10000, days=5, max=15):
        urls = self.get_related_articles(doc,n)
        article_map = self.article_loader.article_map
        if not reference_day:
            reference_day= date.today()
        recent_urls = []
        for url in urls:
            record = article_map[url]

            diff_in_days = abs(reference_day -record["date_p"]).days

            if (diff_in_days <= days):
                recent_urls.append(url)
            if (len(recent_urls) >= max):
                break
        return recent_urls


    def find_related_articles(self, url,  max=15):
        record = self.article_loader.article_map[url]
        article = record["text"]
        date_record = record["date_p"]

        batch1 = self.get_related_articles_in_interval(article, date_record, 4000, 5, 15)
        batch2 = self.get_related_articles_in_interval(article, date_record, 2000, 10, 15)
        batch3 = self.get_related_articles_in_interval(article, date_record, 1000, 15, 15)
        return (batch1 + batch2 + batch3)[:max]


    def interesting_articles_for_day(self, start, end):
        urls_of_day = self.article_loader.articles_in_interval(start, end)
        all_links = []
        for url in urls_of_day:
            ars_score = self.get_related_articles_and_score(url,2500,4)
            sum_score = sum([x[1] for x in ars_score])
            str_score = str(round(sum_score,2))

            len_article = len(self.article_loader.article_map[url]["text"])
            #sum_score += len_article / 400
            #str_score = str_score + "+"+str(len_article)+"/500"
            all_links.append((url, round(sum_score,2), str_score, [x[0] for x in ars_score ]))
        sall_links = sorted(all_links, key = lambda x: x[1], reverse=True)
        return sall_links