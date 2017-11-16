# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request



from datetime import date


from itertools import chain
from . import end_condition, build_text_from_paragraphs, already_crawled


class ArstechnicaSpider(scrapy.Spider):
    name = "arstechnica"
    pages_V = set()
    urls_V = set()
    allowed_domains = ["arstechnica.com"]
    start_urls = (
        'https://arstechnica.com/','http://arstechnica.com/'
    )



    def __init__(self, article_repo, go_back_date, url_list = None):
        super().__init__()
        self.article_repo = article_repo
        self.go_back_date = go_back_date

        self.finished = False
        self.url_list = url_list


    def parse(self, response):
        if self.url_list:
            for url in self.url_list:
                yield Request(url , callback=self.parse_page,
                          meta={'URL': url})
        else:


            url1s = response.xpath('//a[@class="overlay"]/@href').extract()
            url2s = response.xpath('//h2/a/@href').extract()

            pages = response.xpath('//div[@class="prev-next-links"]/a/@href').extract()


            for url in chain(url1s, url2s):

                absolute_url = response.urljoin(url)
                if (absolute_url not in self.urls_V and not already_crawled(self.article_repo, absolute_url)):
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
        article_title = "".join(article_title_parts).strip()
        #all_paragraphs = response.xpath('//div[@itemprop="articleBody"]//p/text()|//div[@itemprop="articleBody"]//p/em//text()|//div[@itemprop="articleBody"]//p/a//text()|//div[@itemprop="articleBody"]//p/i//text()').extract()
        first_paragraph = response.xpath(
            '//div[@itemprop="articleBody"]/text()').extract()
        all_paragraphs = response.xpath(
            '//div[@itemprop="articleBody"]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure)  and not(.//script)]//text()').extract()
        article_authors = response.xpath('//a[@rel="author"]/@href').extract()

        article_datetime_tsstring = response.xpath('//time/@datetime').extract_first()


        article_date_str = article_datetime_tsstring.split('T')[0]
        article_date = date(*map(int,article_date_str.split('-')))
        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)

        if (end_condition(article_date, self.go_back_date )):
            self.finished = True
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : ""}

