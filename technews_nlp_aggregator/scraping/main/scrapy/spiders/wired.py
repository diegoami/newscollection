# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled
from datetime import date




class WiredSpider(scrapy.Spider):
    name = "wired"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["wired.com"]
    start_urls = (
        'https://www.wired.com/', 'http://www.wired.com/'
    )


    def __init__(self, article_repo, go_back_date, url_list=None):
        super().__init__()
        self.article_repo = article_repo
        self.go_back_date = go_back_date

        self.finished = False
        self.url_list = url_list


    def parse(self, response):
        if self.url_list:
            for url in self.url_list:
                yield Request(url, callback=self.parse_page,
                              meta={'URL': url})
        else:
            urls = response.xpath('//h2[contains(@class,"archive-item-component__link")]/@href').extract()


            for url in urls:
                absolute_url = response.urljoin(url)
                article_date = extract_date(url)
                if (article_date):
                    if (absolute_url not in self.urls_V and not already_crawled(self.article_repo, absolute_url)):
                        self.urls_V.add(absolute_url)
                        yield Request(absolute_url, callback=self.parse_page,
                                      meta={'URL': absolute_url})
            absolute_page = 'https://www.wired.com/most-popular/'
            if (absolute_page not in self.pages_V):
                self.pages_V.add(absolute_page)

                yield Request(absolute_page, callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@class="title"]//text()').extract_first()
        article_title = "".join(article_title_parts).strip()

        all_paragraphs = response.xpath(
            "//article[contains(@class, 'article-body-component')]/div//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()
        article_date_str = response.xpath("//li/time[@class='date-mdy']//text()").extract_first()
        article_authors = response.xpath('//a[@rel="author"]/@href').extract_first()
        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)
        month, day, year = map(int, article_date_str.split('.'))
        article_date = date(year+2000, month, day)


        if (end_condition(article_date, self.go_back_date)):

            self.finished = True
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : []}


