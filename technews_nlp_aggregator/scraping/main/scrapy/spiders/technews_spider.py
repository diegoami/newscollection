# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from . import extract_date, end_condition, build_text_from_paragraphs
from abc import abstractmethod

class TechnewsSpiderHelper():
    pages_V = set()
    urls_V = set()

    def __init__(self, article_repo, go_back_date):
        super().__init__()
        self.article_repo = article_repo
        self.go_back_date = go_back_date

        self.finished = False

    def already_retrieved(self, url):
        retrieved = self.articleLoader.articlesDF.any(self.articleLoader.articlesDF['url'] == url)
        if (retrieved):
            logging.info("{} already retrieved, skipping".format(url))
            return True
        else:
            return False

    def iterate_urls(self, urls, response):
        logging.info("Calling iterate_urls with {}".format(urls))
        for url in urls:

            absolute_url = response.urljoin(url)
            if (self.condition_on_url(url)):
                if (absolute_url not in self.urls_V and not self.already_retrieved(url)):
                    self.urls_V.add(absolute_url)

                    yield Request(absolute_url, callback=self.parse_page,
                                  meta={'URL': absolute_url})

    def iterate_pages(self, pages, response):
        logging.info("Calling iterate_pages with {}".format(pages))
        if not self.finished:
            for page in pages:
                absolute_page = response.urljoin(page)
                if (absolute_page not in self.pages_V):
                    self.pages_V.add(absolute_page)
                    yield Request(absolute_page , callback=self.parse)


    def process_item(self, item):
        if (end_condition(item["date"], self.go_back_date)):
            self.finished = True
        yield item



    @abstractmethod
    def retrieve_urls_and_pages(self, response):
        pass

    @abstractmethod
    def create_item(self, response, url):
        pass

    def condition_on_url(self, url):
        return True



    def parse(self, response):
        urls, pages = self.retrieve_urls_and_pages(response)

        self.iterate_urls(urls, response)
        self.iterate_pages(urls, response)
        logging.info("Leaving parse ...")

    def parse_page(self, response):
        url = response.meta.get('URL')
        item = self.create_item(response, url)
        self.process_item(item)
        logging.info("Leaving parse page...")