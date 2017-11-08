# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from string import punctuation
from time import sleep
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from . import extract_date, end_condition, build_text_from_paragraphs, TechnewsSpiderHelper




class ThenextwebSpider(scrapy.Spider):
    name = "thenextweb"
    pages_C =  0

    allowed_domains = ["thenextweb.com"]
    start_urls = (
        'https://thenextweb.com/','http://thenextweb.com/'
    )


    def __init__(self, article_repo, go_back_date):
        super().__init__( article_repo, go_back_date)


    def retrieve_urls_and_pages(self, response):


        urls = response.xpath('//h4[@class="story-title"]/a/@href').extract()
        pages = ['https://thenextweb.com/latest/page/'+str(self.pages_C)]
        self.pages_C += 1
        return urls, pages

    def condition_on_url(self, url):
        return extract_date(url)

    def create_item(self, response, url):
        url = response.meta.get('URL')
        item = {"url": url}
        article_title_parts = response.xpath('//h1[@class="u-m-0_25"]//text()').extract()
        item["title"] = "".join(article_title_parts)

        all_paragraphs = response.xpath(
            "//div[contains(@class, 'post-body')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure)]//text()").extract()
        item["authors"] = response.xpath('//a[@class="post-authorName"]/@href').extract()
        item["tags"] = response.xpath("//span[contains(@class, 'tag')]/a/@href").extract()

        item["text"] = build_text_from_paragraphs(all_paragraphs)

        item["date"] = extract_date(url)
        return item

