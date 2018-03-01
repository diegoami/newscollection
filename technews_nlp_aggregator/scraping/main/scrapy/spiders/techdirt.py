# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request

from . import end_condition, build_text_from_paragraphs, get_date_from_string, get_date_from_string_mdy

class TechdirtSpider(scrapy.Spider):
    name = "techdirt"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["techdirt.com"]
    start_urls = (
        'https://www.techdirt.com/', 'http://www.techdirt.com/'
    )

    def __init__(self, article_repo, go_back_date, url_list=None):
        super().__init__()
        self.article_repo = article_repo
        self.go_back_date = go_back_date

        self.finished = 0
        self.url_list = url_list


    def parse(self, response):
        if self.url_list:
            for url in self.url_list:
                yield Request(url, callback=self.parse_page,
                              meta={'URL': url})

    def parse_page(self, response):
        url = response.meta.get('URL')

        article_title_parts = response.xpath("//h1[contains(@class, 'posttitle')]//text()").extract_first()
        article_title = "".join(article_title_parts ).strip()
        all_paragraphs = response.xpath(
            "//div[contains(@class, 'postbody')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()
        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)
        article_date_str_t = response.xpath("//p[contains(@class, 'storydate')]//text()").extract_first()
        article_date = get_date_from_string_mdy(article_date_str_t)
        if (end_condition(article_date, self.go_back_date)):
            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": [], "date" :article_date, "filename" : "", "tags" : []}