# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request
import re
import calendar

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled, get_date_from_string

from . import TechControversySpider
class IncSpider(TechControversySpider):
    name = "inc"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["inc.com"]
    start_urls = (
        'https://www.inc.com/', 'http://www.inc.com/'
    )

    def __init__(self, article_repo, go_back_date, url_list):
        super().__init__(article_repo, go_back_date, url_list)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1//span//text()').extract()
        article_title = "".join(article_title_parts).strip()
        all_paragraphs = response.xpath(
            "//div[contains(@class, 'article-body')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()

        all_paragraph_text = build_text_from_paragraphs( all_paragraphs)
        article_datetime_ts = response.xpath("//div[contains(@class, 'ArticlePubdate')]//text()").extract_first()
        published, date_str = article_datetime_ts.split(':')
        article_date = get_date_from_string(date_str)

        if (end_condition(article_date, self.go_back_date)):

            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": "", "date" :article_date, "filename" : "", "tags" : []}


