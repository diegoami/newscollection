# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from time import sleep

from datetime import datetime,date
from string import punctuation
from . import extract_date
from itertools import chain



class TechcrunchSpider(scrapy.Spider):
    name = "jobs"
    pages_V = set()
    urls_V = set()
    allowed_domains = ["techcrunch.com"]
    start_urls = (
        'https://techcrunch.com/','http://techcrunch.com/'
    )


    def __init__(self, article_repo):
        super().__init__()
        self.article_repo = article_repo
        self.finished = False


    def parse(self, response):



        urls = response.xpath('//h2[@class="post-title"]/a/@href').extract()

        pages = response.xpath('//li[@class="next"]/a/@href').extract()

        for url in urls:
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
        article_title_parts = response.xpath('//h1[@class="alpha tweet-title"]//text()').extract()
        article_title = "".join(article_title_parts)

        all_paragraphs = response.xpath(
            "//div[contains(@class, 'article-entry')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure)]//text()").extract()
        article_authors = response.xpath('//a[@rel="author"]/@href').extract()
        article_tags = response.xpath("//div[contains(@class, 'loaded') or @class='tag-item']/a/@href").extract()


        article_date = extract_date( url)
        all_paragraph_text = ""
        skip_next = False
        for paragraph in all_paragraphs:
            if len(paragraph) == 0 or paragraph[0] == '\n':
                continue
            if (paragraph[-1] in ".!?"):
                paragraph = paragraph + "\n"
            elif (paragraph[-1] in punctuation):
                paragraph = paragraph + " "

            all_paragraph_text = all_paragraph_text+paragraph

        sleep(1)

        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : article_tags}

