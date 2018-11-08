# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from . import extract_date, end_condition, build_text_from_paragraphs, build_from_timestamp


class MashableSpider(scrapy.Spider):
    name = "mashable"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["mashable.com"]
    start_urls = (
        'https://mashable.com/', 'http://mashable.com/'
    )


    def __init__(self, article_repo, go_back_date, url_list):
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
        else:
            pass





    def parse_page(self, response):
        url = response.meta.get('URL')

        article_title_parts = response.xpath("//h1[contains(@class, 'title')]/text()").extract()
        article_title = "".join(article_title_parts ).strip()
        all_paragraphs = response.xpath(
            "//section[contains(@class, 'article-content')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class='see-also']) and not(.//p[@class='see-also-link']) and not(contains(@class,'see-also-link'))]//text()").extract()


        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)

        article_datetime_ts = response.xpath("//time/text()").extract_first()

        article_date = build_from_timestamp(article_datetime_ts, ' ')
        if (end_condition(article_date, self.go_back_date)):
            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": [] , "date" :article_date, "filename" : "", "tags" : []}


