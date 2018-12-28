# -*- coding: utf-8 -*-
from datetime import date

import scrapy
from scrapy import Request

from . import end_condition, build_text_from_paragraphs

from . import TechControversySpider
class GizmodoSpider(TechControversySpider):
    name = "gizmodo"
    finished = 0
    pages_C = 0
    skipped = 0

    urls_V = set()
    pages_V = set()
    allowed_domains = ["gizmodo.com"]
    start_urls = (
        'https://gizmodo.com/', 'http://gizmodo.com/', 'http://fieldguide.gizmodo.com/'
    )


    def __init__(self, article_repo, go_back_date, url_list = None):
        super().__init__(article_repo, go_back_date, url_list)



    def parse_page(self, response):
        url = response.meta.get('URL')

        article_title_parts = response.xpath("//h1[contains(@class, 'headline')]/a/text()").extract()
        article_title = "".join(article_title_parts ).strip()
        all_paragraphs = response.xpath(
            "//div[contains(@class, 'post-content')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()


        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)

        article_date_str_l = response.xpath("//div/time[contains(@class, 'meta__time')]/a/@title").extract_first()
        article_date_str = article_date_str_l.split()[0]
        article_authors = response.xpath("//div[contains(@class, 'author')]/a/@href").extract_first()
        month, day, year = map(int, article_date_str.split('/'))
        article_date = date(year + 2000, month, day)

        if (end_condition(article_date, self.go_back_date)):
            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors , "date" :article_date, "filename" : "", "tags" : []}


