# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from . import extract_date, end_condition, build_text_from_paragraphs
from . import TechnewsSpiderHelper

class TechcrunchSpider(scrapy.Spider):
    name = "techcrunch"
    allowed_domains = ["techcrunch.com"]
    start_urls = (
        'https://techcrunch.com/','http://techcrunch.com/'
    )
    pages_V = set()
    urls_V = set()

    def __init__(self, article_repo, article_loader,  go_back_date):
        super().__init__()
        self.article_loader = article_loader
        self.article_repo = article_repo
        self.go_back_date = go_back_date

        self.finished = False


    def retrieve_urls_and_pages(self, response):
        urls = response.xpath('//h2[@class="post-title"]/a/@href').extract()
        pages = response.xpath('//li[@class="next"]/a/@href').extract()
        return urls, pages

    def condition_on_url(self, url):
        return extract_date(url)

    def create_item(self, response, url):
        item = {}
        item["url"] = url
        article_title_parts = response.xpath('//h1[@class="alpha tweet-title"]//text()').extract()
        item["title"] = "".join(article_title_parts)
        all_paragraphs_r = response.xpath(
            "//div[contains(@class, 'article-entry')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure)]//text()")
        all_paragraphs = all_paragraphs_r.extract()
        item["authors"] = response.xpath('//a[@rel="author"]/@href').extract()
        item["tags"]= response.xpath("//div[contains(@class, 'loaded') or @class='tag-item']/a/@href").extract()

        item["date"] = extract_date(url)
        item["text"] = build_text_from_paragraphs(all_paragraphs)
        return item

    def parse(self, response):
        urls, pages = self.retrieve_urls_and_pages(response)

        for u in self.iterate_urls(urls, response):
            yield u
        for p in self.iterate_pages(urls, response):
            yield p

    def parse_page(self, response):
        url = response.meta.get('URL')
        item = self.create_item(response, url)
        for i in self.process_item(item):
            yield i
        logging.info("Leaving parse page...")

    def already_retrieved(self, url):
        retrieved = len(self.article_loader.articlesDF['url'] == url) > 0
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
                    yield Request(absolute_page, callback=self.parse)

    def process_item(self, item):
        if (end_condition(item["date"], self.go_back_date)):
            self.finished = True
        yield item