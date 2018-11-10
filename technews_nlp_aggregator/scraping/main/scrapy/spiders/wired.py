# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled, build_from_timestamp, get_simple_date

from . import TechControversySpider
class WiredSpider(TechControversySpider):
    name = "wired"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["wired.com"]
    start_urls = (
        'https://www.wired.com/', 'http://www.wired.com/'
    )

    def __init__(self, article_repo, go_back_date, url_list=None):
        super().__init__(article_repo, go_back_date, url_list)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1//text()').extract_first()
        article_title = "".join(article_title_parts).strip()

        all_paragraphs = response.xpath(
            "//div[contains(@class, 'article')]/div//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()

        article_authors = ""
        article_datetime_ts = response.xpath('//time/text()').extract_first()

        article_date = get_simple_date(article_datetime_ts)
        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)


        if (end_condition(article_date, self.go_back_date)):

            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : []}


