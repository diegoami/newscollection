# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request
import re
import calendar

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled, build_from_timestamp

from . import TechControversySpider
class InverseSpider(TechControversySpider):
    name = "inverse"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["inverse.com"]
    start_urls = (
        'https://www.inverse.com/', 'http://www.inverse.com/'
    )

    def __init__(self, article_repo, go_back_date, url_list):
        super().__init__(article_repo, go_back_date, url_list)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath("//h1[contains(@class, 'banner-title')]//text()").extract()
        article_title = "".join(article_title_parts).strip()
        all_paragraph_before = response.xpath("//div[contains(@h2, 'banner-dek')]//text()").extract()
        all_paragraphs = response.xpath(
            "//section[contains(@class, 'art-body')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()
        all_paragraph_text = build_text_from_paragraphs( all_paragraph_before  + all_paragraphs )
        article_datetime_ts = response.xpath('//time/@datetime').extract_first()
        article_authors = response.xpath("//address[contains(@class, 'art-author')]/a/@href").extract()

        article_date = build_from_timestamp(article_datetime_ts)

        if (end_condition(article_date, self.go_back_date)):

            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors , "date" :article_date, "filename" : "", "tags" : []}


