# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request



from datetime import date


from itertools import chain
from . import  build_text_from_paragraphs, TechnewsSpiderHelper

class ArstechnicaSpider(scrapy.Spider):
    name = "arstechnica"

    allowed_domains = ["arstechnica.com"]
    start_urls = (
        'https://arstechnica.com/','http://arstechnica.com/'
    )

    def retrieve_urls_and_pages(self, response):
        url1s = response.xpath('//a[@class="overlay"]/@href').extract()
        url2s = response.xpath('//h2/a/@href').extract()

        pages = response.xpath('//div[@class="prev-next-links"]/a/@href').extract()

        return chain(url1s, url2s), pages



    def create_item(self, response, url):
        item = {}
        item["url"] = url
        article_title_parts = response.xpath('//h1[@class="alpha tweet-title"]//text()').extract()
        item["title"] = "".join(article_title_parts)
        all_paragraphs_r = response.xpath(
            "//div[contains(@class, 'article-entry')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure)]//text()")
        all_paragraphs = all_paragraphs_r.extract()
        item["authors"] = response.xpath('//a[@rel="author"]/@href').extract()
        item["tags"] = response.xpath("//div[contains(@class, 'loaded') or @class='tag-item']/a/@href").extract()

        item["date"] = extract_date(url)
        item["text"] = build_text_from_paragraphs(all_paragraphs)
        return item

    def __init__(self, article_repo, go_back_date):
        super().__init__(article_repo, go_back_date)




    def parse_page(self, response):
        url = response.meta.get('URL')
        item = {}
        item["url"] = url
        article_title_parts = response.xpath('//h1[@itemprop="headline"]//text()').extract()
        item["title"] = "".join(article_title_parts)

        all_paragraphs = response.xpath(
            '//div[@itemprop="articleBody"]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure)]//text()').extract()
        item["authors"]= response.xpath('//a[@rel="author"]/@href').extract()

        article_datetime_tsstring = response.xpath('//time/@datetime').extract_first()


        article_date_str = article_datetime_tsstring.split('T')[0]
        item["date"] = date(*map(int,article_date_str.split('-')))
        item["text"] = build_text_from_paragraphs(all_paragraphs)
        return item