# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request
import re
import calendar

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled, build_from_timestamp

from . import TechControversySpider
class QzSpider(TechControversySpider):
    name = "qz"
    finished = 0
    pages_C = 0
    skipped = 0

    urls_V = set()
    pages_V = set()
    allowed_domains = ["qz.com"]
    start_urls = (
        'https://qz.com/', 'http://qz.com/'
    )

    def __init__(self, article_repo, go_back_date, url_list):
        super().__init__(article_repo, go_back_date, url_list)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1//text()').extract()
        article_title = "".join(article_title_parts).strip()
        all_paragraphs = response.xpath(
            "//article//div//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()

        all_paragraph_text = build_text_from_paragraphs( all_paragraphs)
        article_datetime_ts = response.xpath('//time/@datetime').extract_first()

        article_date = build_from_timestamp(article_datetime_ts)

        if (end_condition(article_date, self.go_back_date)):

            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": [], "date" :article_date, "filename" : "", "tags" : []}


