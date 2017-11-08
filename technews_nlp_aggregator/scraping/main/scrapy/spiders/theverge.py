# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from . import extract_date,  end_condition, build_text_from_paragraphs, TechnewsSpiderHelper



class ThevergeSpider(scrapy.Spider):
    name = "theverge"
    pages_C =  0
    allowed_domains = ["theverge.com"]
    start_urls = (
        'https://www.theverge.com/', 'http://www.theverge.com/'
    )

    def __init__(self, article_repo, go_back_date):
        super().__init__(article_repo, go_back_date)

    def retrieve_urls_and_pages(self, response):

        urls = response.xpath('//h3/a/@href').extract()
        pages = ['https://www.theverge.com/archives/' + str(self.pages_C)]
        self.pages_C += 1
        return urls, pages

    def condition_on_url(self, url):
        return extract_date(url)

    def create_item(self, response, url):
        url = response.meta.get('URL')
        item = {"url" : url}
        article_title_parts = response.xpath('//h1[@class="c-page-title"]//text()').extract()
        item["title"] = "".join(article_title_parts)

        all_paragraphs = response.xpath(
            "//div[contains(@class, 'c-entry-content')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(./div/twitterwidget)]//text()").extract()
        item["authors"] = response.xpath('//div[@class="c-byline"]/span[@class="c-byline__item"]/a/@href').extract()
        item["tags"] = response.xpath("//li[contains(@class, 'c-entry-group-labels__item')]/a/@href").extract()

        item["text"] = build_text_from_paragraphs(all_paragraphs)

        item["date"] = extract_date(url)
        return item



