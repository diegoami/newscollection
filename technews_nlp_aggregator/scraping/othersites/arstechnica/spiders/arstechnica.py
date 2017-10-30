# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from time import sleep

from datetime import datetime,date
from string import punctuation

from itertools import chain

def end_condition(date):
    if date.month < 10 or date.day < 15:
        return True
    else:
        return False


class ArstechnicaSpider(scrapy.Spider):
    name = "arstechnica"
    pages_V = set()
    urls_V = set()
    allowed_domains = ["arstechnica.com"]
    start_urls = (
        'https://arstechnica.com/','http://arstechnica.com/'
    )



    def __init__(self, article_repo):
        super().__init__()
        self.article_repo = article_repo
        self.finished = False


    def parse(self, response):



        url1s = response.xpath('//a[@class="overlay"]/@href').extract()
        url2s = response.xpath('//h2/a/@href').extract()

        pages = response.xpath('//div[@class="prev-next-links"]/a/@href').extract()

        for url in chain(url1s, url2s):

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
        article_title_parts = response.xpath('//h1[@itemprop="headline"]//text()').extract()
        article_title = "".join(article_title_parts)
        #all_paragraphs = response.xpath('//div[@itemprop="articleBody"]//p/text()|//div[@itemprop="articleBody"]//p/em//text()|//div[@itemprop="articleBody"]//p/a//text()|//div[@itemprop="articleBody"]//p/i//text()').extract()
        all_paragraphs = response.xpath(
            '//div[@itemprop="articleBody"]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure)]//text()').extract()
        article_authors = response.xpath('//a[@rel="author"]/@href').extract()

        article_datetime_tsstring = response.xpath('//time/@datetime').extract_first()


        article_date_str = article_datetime_tsstring.split('T')[0]
        article_date = date(*map(int,article_date_str.split('-')))
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
        if (end_condition(article_date)):
            self.finished = True
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : ""}

