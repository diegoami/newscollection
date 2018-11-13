# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging


from datetime import date

from . import TechControversySpider
from itertools import chain
from . import end_condition, build_text_from_paragraphs, already_crawled


class ArstechnicaSpider(TechControversySpider):
    name = "arstechnica"
    pages_V = set()
    urls_V = set()
    pages_C = 0
    allowed_domains = ["arstechnica.com"]
    start_urls = (
        'https://arstechnica.com/','http://arstechnica.com/'
    )



    def __init__(self, article_repo, go_back_date, url_list = None):
        super().__init__(article_repo, go_back_date, url_list )



    def parse(self, response):
        super().parse(response)
        url1s = response.xpath('//a[@class="overlay"]/@href').extract()
        url2s = response.xpath('//h2/a/@href').extract()

        pages = response.xpath('//div[@class="prev-next-links"]/a/@href').extract()
        for url in chain(url1s, url2s):
            absolute_url = response.urljoin(url)
            if (absolute_url not in self.urls_V and not already_crawled(self.article_repo, absolute_url)):
                self.urls_V.add(absolute_url)

                yield Request(absolute_url, callback=self.parse_page,
                              meta={'URL': absolute_url})
            else:
                article_date = self.article_repo.url_date(absolute_url)
                if (end_condition(article_date, self.go_back_date)):
                    logging.info("Found article at date {}, finishing crawling".format(article_date))
                    self.finished += 1
                else:
                    self.skipped += 1
        if self.crawl_allowed():
            for page in pages:
                absolute_page = response.urljoin(page)
                if (absolute_page not in self.pages_V):
                    self.pages_V.add(absolute_page)
                    self.pages_C += 1
                    yield Request(absolute_page , callback=self.parse)



    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@itemprop="headline"]//text()').extract()
        article_title = " ".join([x for x in article_title_parts if "ars_ab" not in x]).strip()
        #all_paragraphs = response.xpath('//div[@itemprop="articleBody"]//p/text()|//div[@itemprop="articleBody"]//p/em//text()|//div[@itemprop="articleBody"]//p/a//text()|//div[@itemprop="articleBody"]//p/i//text()').extract()
        all_paragraph_before = response.xpath('//h2[@itemprop="description"]//text()').extract()
        first_paragraph = response.xpath(
            '//div[@itemprop="articleBody"]/text()').extract()
        all_paragraphs = response.xpath(
            '//div[@itemprop="articleBody"]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure)  and not(.//script)]//text()').extract()
        article_authors = response.xpath('//a[@rel="author"]/@href').extract()

        article_datetime_tsstring = response.xpath('//time/@datetime').extract_first()


        article_date_str = article_datetime_tsstring.split('T')[0]
        article_date = date(*map(int,article_date_str.split('-')))
        all_paragraph_text = build_text_from_paragraphs( all_paragraph_before + all_paragraphs)

        if (end_condition(article_date, self.go_back_date )):
            self.finished += 1


        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : ""}

