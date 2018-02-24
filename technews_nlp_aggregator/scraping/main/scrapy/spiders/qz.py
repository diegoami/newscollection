# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request
import re
import calendar

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled


class QzSpider(scrapy.Spider):
    name = "qz"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["qz.com"]
    start_urls = (
        'https://qz.com/', 'http://qz.com/'
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
            urls = response.xpath('//div[@class="homepage-main"]/a/@href').extract()


            for url in urls:
                absolute_url = response.urljoin(url)
                article_date = extract_date(url)
                if (article_date):
                    if (absolute_url not in self.urls_V and not already_crawled(self.article_repo, absolute_url)):
                        self.urls_V.add(absolute_url)
                        yield Request(absolute_url, callback=self.parse_page,
                                      meta={'URL': absolute_url})





    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@itemprop="headline"]//text()').extract()
        article_title = "".join(article_title_parts).strip()
        all_paragraphs = response.xpath(
            "//div[contains(@class, 'item-body')]/div//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()
        article_date_str_l = response.xpath("//p[contains(@class, 'storydate')]//text()").extract_first()
        article_authors = response.xpath('//a[@class="author-name"]/@href').extract_first()
        all_paragraph_text = build_text_from_paragraphs( all_paragraphs)
        month_name, day, year= re.split('\W+', article_date_str_l)
        month = list(calendar.month_name).index(month_name)
        article_date = date(int(year), month, int(day))


        if (end_condition(article_date, self.go_back_date)):

            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : []}


