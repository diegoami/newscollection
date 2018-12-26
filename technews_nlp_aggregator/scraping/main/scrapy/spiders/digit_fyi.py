# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request

from . import extract_date, end_condition, build_text_from_paragraphs, build_from_timestamp

from . import TechControversySpider
class DigitSpider(TechControversySpider):
    name = "digit"
    finished = 0
    pages_C = 0
    skipped = 0

    urls_V = set()
    pages_V = set()
    allowed_domains = ["digit.fyi"]
    start_urls = (
        'http://digit.fyi/', 'https://digit.fyi/'   )

    def __init__(self, article_repo, go_back_date, url_list):
        super().__init__(article_repo, go_back_date, url_list)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@class="page-title"]//text()').extract()
        article_title = "".join(article_title_parts).strip()
        all_paragraph_before = response.xpath('//div[@class="page-intro"]//text()').extract()
        all_paragraphs = response.xpath(
            '//div[@class="general-content"]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()').extract()
        all_paragraph_text = build_text_from_paragraphs(all_paragraph_before + all_paragraphs)

        article_date_str_l = response.xpath('//meta[@property="article:published_time"]/@content').extract_first()
        article_date = build_from_timestamp(article_date_str_l)
        if (end_condition(article_date, self.go_back_date)):
            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": [], "date" :article_date, "filename" : "", "tags" : []}


