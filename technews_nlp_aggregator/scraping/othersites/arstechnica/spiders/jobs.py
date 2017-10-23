# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import os
from time import time
from time import sleep
import json

from technews_nlp_aggregator.scraping.technews_retriever import url_to_filename
from datetime import datetime,date


from itertools import chain



class JobsSpider(scrapy.Spider):
    name = "jobs"
    pages_V = set()
    urls_V = set()
    allowed_domains = ["arstechnica.com"]
    start_urls = (
        'https://arstechnica.com/','http://arstechnica.com/'
    )
    finished = False



    def parse(self, response):



        url1s = response.xpath('//a[@class="overlay"]/@href').extract()
        url2s = response.xpath('//h2/a/@href').extract()

        pages = response.xpath('//div[@class="prev-next-links"]/a/@href').extract()

        for url in chain(url1s, url2s):
            if "/2016/" in url:
                self.finished = True
            absolute_url = response.urljoin(url)
            if (absolute_url not in self.urls_V):
                self.urls_V.add(absolute_url)

                yield Request(absolute_url, callback=self.parse_page,
                              meta={'URL': absolute_url})



        if not self.finished:
            for page in pages:
                absolute_page = response.urljoin(page)
                if (absolute_page not in self.pages_V):
                    self.pages_V.add(absolute_page)
                    yield Request(absolute_page , callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        all_paragraphs = response.xpath('//div[@itemprop="articleBody"]/p/text()').extract()
        article_authors = response.xpath('//a[@rel="author"]/@href').extract()

        article_datetime_tsstring = response.xpath('//time/@datetime').extract_first()


        article_date_str = article_datetime_tsstring.split('T')[0]
        article_date = date(*map(int,article_date_str.split('-')))
        all_paragraph_text = "\n".join(
            [x for x in all_paragraphs if len(x) > 0 and not x[0] == '\n'])
        sleep(1)
        yield {"title": article_title, "text": all_paragraph_text, "authors": article_authors, "date" :article_date}

