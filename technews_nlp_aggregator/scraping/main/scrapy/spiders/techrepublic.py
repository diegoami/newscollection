# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from datetime import date
from . import extract_date, end_condition, build_text_from_paragraphs, get_date_from_string, TechnewsSpiderHelper



class TechrepublicSpider(scrapy.Spider):
    name = "techrepublic"

    pages_C = 0

    allowed_domains = ["techrepublic.com" ]
    start_urls = (
        'http://www.techrepublic.com','https://www.techrepublic.com'
    )

    def retrieve_urls_and_pages(self, response):
        urls = response.xpath('//h3[@class="title"]/a/@href').extract()
        pages = ['http://www.techrepublic.com/' + str(self.pages_C)]
        self.pages_C += 1
        return urls, pages

    def create_item(self, response, url):
        item = {"url" : url}
        article_title_parts = response.xpath('//h1[@class="title"]//text()').extract()
        item["title"] = "".join(article_title_parts)
        all_paragraphs_r = response.xpath(
            "//div[contains(@class, 'content') and contains(@data-component, 'lazyloadImages')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure)]//text()")
        all_paragraphs = all_paragraphs_r.extract()
        item["authors"] = response.xpath('//a[@rel="author"]/@href').extract()
        item["tags"] = response.xpath("//p[contains(@class, 'categories')]/a/@href").extract()
        article_date_str = response.xpath("//span[@class='date']//text()").extract_first()

        item["date"] = get_date_from_string(article_date_str)

        item["text"] = build_text_from_paragraphs(all_paragraphs, punct_add_point=")")
        return item

    def __init__(self, article_repo, go_back_date):
        super().__init__(article_repo, go_back_date)



