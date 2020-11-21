
import scrapy
import logging
from scrapy import Request



from . import end_condition, build_text_from_paragraphs, get_date_from_string

class TechControversySpider(scrapy.Spider):
    finished = 0
    pages_C = 0
    skipped = 0


    def __init__(self, article_repo, go_back_date, url_list = None):
        super().__init__()
        self.article_repo = article_repo
        self.go_back_date = go_back_date
        self.url_list = url_list


    def parse(self, response):
        if self.url_list:
            for url in self.url_list:
                yield Request(url, callback=self.parse_page,
                              meta={'URL': url,  'dont_redirect': True,
                                    'handle_httpstatus_list': [301,302,307]})
        else:
            for r in self.parse_crawl(response):
                yield r

    def parse_crawl(self, response):
        raise NotImplementedError()

    def parse_page(self):
        pass


    def crawl_allowed(self):
        allowed = self.finished < 20 and self.pages_C < 150 and self.skipped < 250
        logging.info("{}: Crawl allowed: {} ( {} finished < 5, {} pages_C < 150, {} skipped < 250".format(self.__class__.__name__, allowed,  self.finished, self.pages_C, self.skipped))
        return allowed


    def request_for_next_page(self):
        absolute_page = self.get_next_page()
        self.pages_C += 1

        logging.info("Adding absolute page " + absolute_page)
        if (absolute_page not in self.pages_V):
            self.pages_V.add(absolute_page)

            return Request(absolute_page, callback=self.parse)
