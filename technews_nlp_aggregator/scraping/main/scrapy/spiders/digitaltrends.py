# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled

from . import TechControversySpider
class DigitaltrendsSpider(TechControversySpider):
    name = "digitaltrends"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["digitaltrends.com"]
    start_urls = (
        'https://www.digitaltrends.com', 'http://www.digitaltrends.com'
    )

    def __init__(self, article_repo, go_back_date, url_list):
        super().__init__(article_repo, go_back_date, url_list)



    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath("//h1[contains(@itemprop, 'headline')]//text()").extract_first()
        article_title = "".join(article_title_parts).strip()

        all_paragraphs = response.xpath(
            "//article[contains(@itemprop, 'articleBody')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[contains(@class, 'm-newsletter-minimal')])]//text()").extract()
        article_datetime_ts = response.xpath("//time/@datetime").extract_first()

        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)
        article_date_str = article_datetime_ts.split('T')[0]
        article_date = date(*map(int,article_date_str.split('-')))

        if (end_condition(article_date, self.go_back_date)):

            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": [], "date" :article_date, "filename" : "", "tags" : []}


