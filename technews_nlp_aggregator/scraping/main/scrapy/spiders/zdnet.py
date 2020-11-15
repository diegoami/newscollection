# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled

from . import TechControversySpider
class ZdnetSpider(TechControversySpider):
    name = "zdnet"
    finished = 0
    pages_C = 0
    skipped = 0

    urls_V = set()
    pages_V = set()
    allowed_domains = ["zdnet.com"]
    start_urls = (
        'https://www.zdnet.com/', 'http://www.zdnet.com/'   )

    def __init__(self, article_repo, go_back_date, url_list):
        super().__init__(article_repo, go_back_date, url_list)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1//text()').extract()
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
            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : []}


