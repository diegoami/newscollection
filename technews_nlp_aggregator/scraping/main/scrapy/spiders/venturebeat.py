# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from . import extract_date, end_condition, build_text_from_paragraphs, TechnewsSpiderHelper




class VenturebeatSpider(scrapy.Spider):
    name = "venturebeat"
    pages_C =  0
    allowed_domains = ["venturebeat.com"]
    start_urls = (
        'https://venturebeat.com/', 'http://venturebeat.com/'
    )

    def __init__(self, article_repo, go_back_date):
        super().__init__(article_repo, go_back_date)

    def retrieve_urls_and_pages(self, response):

        urls = response.xpath('//h2[@class="article-title"]/a/@href').extract()
        pages = ['https://venturebeat.com/page/' + str(self.pages_C)]
        self.pages_C += 1
        return urls, pages

    def condition_on_url(self, url):
        return extract_date(url)

    def create_item(self, response, url):
        url = response.meta.get('URL')
        item = {"url" : url}
        article_title_parts = response.xpath('//h1[@class="article-title"]//text()').extract()
        item["title"] = "".join(article_title_parts)

        all_paragraphs = response.xpath(
            "//div[contains(@class, 'article-content')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)]//text()").extract()
        item["authors"] = response.xpath('//div[@class="article-byline"]/a[@rel="author"]/@href').extract()
        item["tags"] = response.xpath("//a[contains(@class, 'article-category')]/@href").extract()

        item["text"] = build_text_from_paragraphs(all_paragraphs)

        item["date"] = extract_date(url)
        return item

