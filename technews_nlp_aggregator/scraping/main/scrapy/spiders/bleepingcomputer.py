# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request
import re
import calendar

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled, get_date_from_string

from . import TechControversySpider
class BleepingcomputerSpider(TechControversySpider):
    name = "bleepingcomputer"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["bleepingcomputer.com"]
    start_urls = (
        'https://www.bleepingcomputer.com/', 'http://www.bleepingcomputer.com/'
    )


    def __init__(self, article_repo, go_back_date, url_list):
        super().__init__(article_repo, go_back_date, url_list)



    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath("//h1//text()").extract()
        article_title = "".join(article_title_parts).strip()
        all_paragraphs = response.xpath(
            "//div[contains(@class, 'articleBody')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()
        article_datetime_ts = response.xpath("//li[contains(@class, 'cz-news-date')]/text()").extract_first()
        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)

        article_date = get_date_from_string(article_datetime_ts)

        if (end_condition(article_date, self.go_back_date)):

            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": [] , "date" :article_date, "filename" : "", "tags" : []}


