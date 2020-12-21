# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request

from . import end_condition, build_text_from_paragraphs, get_date_from_string, build_from_timestamp

from . import TechControversySpider

class ReutersSpider(TechControversySpider):
    name = "reuters"
    finished = 0
    pages_C = 0
    skipped = 0

    urls_V = set()
    pages_V = set()
    allowed_domains = ["reuters.com"]
    start_urls = (
        'https://www.reuters.com/', 'http://www.reuters.com/'
    )

    def __init__(self, article_repo, go_back_date, url_list=None):
        super().__init__(article_repo, go_back_date, url_list)


    def parse_page(self, response):
        url = response.meta.get('URL')

        article_title_parts = response.xpath("//h1//text()").extract_first()
        article_title = "".join(article_title_parts ).strip()

        all_paragraphs = response.xpath(
            "//div[contains(@class, 'ArticleBodyWrapper')]//p[contains(@class, 'ArticleBody-para-TD_9x')]//text()").extract()
        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)
        article_date_text = response.xpath("//meta[@property='og:article:modified_time']/@content").extract_first()

        article_date = build_from_timestamp(article_date_text)

        if (end_condition(article_date, self.go_back_date)):
            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": [], "date" :article_date, "filename" : "", "tags" : []}
