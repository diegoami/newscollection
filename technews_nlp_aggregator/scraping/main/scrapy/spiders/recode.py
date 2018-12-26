# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request
import re
import calendar

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled

from . import TechControversySpider
class RecodeSpider(TechControversySpider):
    name = "recode"
    finished = 0
    pages_C = 0
    skipped = 0

    urls_V = set()
    pages_V = set()
    allowed_domains = ["recode.net"]
    start_urls = (
        'https://www.recode.net/', 'http://www.recode.net/'
    )

    def __init__(self, article_repo, go_back_date, url_list):
        super().__init__(article_repo, go_back_date, url_list)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@class="c-page-title"]//text()').extract()
        article_title = "".join(article_title_parts).strip()
        all_paragraph_before = response.xpath("//h2[contains(@class,'c-entry-summary')]//text()").extract()
        all_paragraphs = response.xpath(
            "//div[contains(@class, 'c-entry-content')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()
        article_date_str_l = response.xpath("//time[@class='c-byline__item']//text()").extract_first()
        article_authors =[]
        all_paragraph_text = build_text_from_paragraphs(  all_paragraph_before + all_paragraphs)
        first, second, third =  article_date_str_l.split(',')
        month_sh_name, day_str = first.split()
        year = int(second)
        month = list(calendar.month_abbr).index(month_sh_name)
        article_date = date(year, month, int(day_str))


        if (end_condition(article_date, self.go_back_date)):

            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : []}


