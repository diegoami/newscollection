# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request

from . import end_condition, build_text_from_paragraphs


class GuardianSpider(scrapy.Spider):
    name = "guardian"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["theguardian.com"]
    start_urls = (
        'https://www.theguardian.com/', 'http://www.theguardian.com/'
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



    def parse_page(self, response):
        url = response.meta.get('URL')

        article_title_parts = response.xpath("//h1[contains(@class, 'content__headline')]//text()").extract_first()
        article_title = "".join(article_title_parts ).strip()
        all_paragraph_before = response.xpath("//div[contains(@class, 'content__standfirst')]/p//text()").extract()
        all_paragraphs = response.xpath(
            "//div[contains(@class, 'content__article-body')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()

        article_datetime_ts = response.xpath('//time/@datetime').extract_first()
        all_paragraph_text = build_text_from_paragraphs(all_paragraph_before + all_paragraphs)


        article_date_str = article_datetime_ts.split('T')[0]
        article_date = date(*map(int,article_date_str.split('-')))
        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)


        if (end_condition(article_date, self.go_back_date)):

            self.finished = True
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": [], "date" :article_date, "filename" : "", "tags" : []}


