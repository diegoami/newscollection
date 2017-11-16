# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled
from datetime import date




class ZdnetSpider(scrapy.Spider):
    name = "zdnet"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["zdnet.com"]
    start_urls = (
        'https://www.zdnet.com/', 'http://www.zdnet.com/'
    )


    def __init__(self, article_repo, go_back_date, url_list):
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
            urls = response.xpath('//div[@class="homepage-main"]/a/@href').extract()


            for url in urls:
                absolute_url = response.urljoin(url)
                article_date = extract_date(url)
                if (article_date):
                    if (absolute_url not in self.urls_V and not already_crawled(self.article_repo, absolute_url)):
                        self.urls_V.add(absolute_url)
                        yield Request(absolute_url, callback=self.parse_page,
                                      meta={'URL': absolute_url})





    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@itemprop="headline"]//text()').extract()
        article_title = "".join(article_title_parts).strip()
        all_paragraph_before = response.xpath("//p[contains(@class, 'summary')]//text()").extract()
        all_paragraphs = response.xpath(
            "//div[contains(@class, 'storyBody')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()
        article_date_str_l = response.xpath("//time/@datetime").extract_first()
        article_authors = response.xpath('//a[@rel="author"]/@href').extract_first()
        all_paragraph_text = build_text_from_paragraphs( all_paragraph_before + all_paragraphs)
        article_date_str = article_date_str_l.split()[0]
        year, month, day = map(int, article_date_str.split('-'))
        article_date = date(year, month, day)


        if (end_condition(article_date, self.go_back_date)):

            self.finished = True
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : []}


