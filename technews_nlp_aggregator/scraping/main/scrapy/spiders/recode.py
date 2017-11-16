# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled
from datetime import date




class GizmodoSpider(scrapy.Spider):
    name = "recode"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["recode.net"]
    start_urls = (
        'https://www.recode.net/', 'http://www.recode.net/'
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
            pass





    def parse_page(self, response):
        url = response.meta.get('URL')

        article_title_parts = response.xpath("//h1[contains(@class, 'c-page-title')]/text()").extract()
        article_title = "".join(article_title_parts ).strip()
        all_paragraph_before = response.xpath("//h2[contains(@class, 'c-entry-summary')]//text()").extract()
        all_paragraphs = response.xpath(
            "//div[contains(@class, 'c-entry-content')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script)//text()").extract()


        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)

        article_date_str_l = response.xpath("//div/time//text()").extract_first()
        article_date_str = article_date_str_l.split()[0]
        article_authors = response.xpath("//div[contains(@class, 'author')]/a/@href").extract_first()
        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)
        month, day, year = map(int, article_date_str.split('/'))
        article_date = date(year + 2000, month, day)


        if (end_condition(article_date, self.go_back_date)):

            self.finished = True
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors , "date" :article_date, "filename" : "", "tags" : []}


