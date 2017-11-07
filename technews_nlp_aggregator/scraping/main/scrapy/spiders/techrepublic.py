# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from datetime import date
from . import extract_date, end_condition, build_text_from_paragraphs, get_date_from_string



class TechrepublicSpider(scrapy.Spider):
    name = "techrepublic"
    pages_V = set()
    pages_C = 0
    urls_V = set()
    allowed_domains = ["techrepublic.com" ]
    start_urls = (
        'http://www.techrepublic.com','https://www.techrepublic.com'
    )

    def __init__(self, article_repo, go_back_date):
        super().__init__()
        self.article_repo = article_repo
        self.go_back_date = go_back_date
        self.finished = False


    def parse(self, response):
        urls = response.xpath('//h3[@class="title"]/a/@href').extract()


        for url in urls:

            absolute_url = response.urljoin(url)
            if (absolute_url not in self.urls_V):
                self.urls_V.add(absolute_url)

                yield Request(absolute_url, callback=self.parse_page,
                              meta={'URL': absolute_url})




        if not self.finished:
            absolute_page = 'http://www.techrepublic.com/'+str(self.pages_C)
            self.pages_C += 1


            logging.info("Adding absolute page "+absolute_page )
            if (absolute_page not in self.pages_V):
                self.pages_V.add(absolute_page)

                yield Request(absolute_page , callback=self.parse)


    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@class="title"]//text()').extract()
        article_title = "".join(article_title_parts)
        all_paragraphs_r = response.xpath(
            "//div[contains(@class, 'content') and contains(@data-component, 'lazyloadImages')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure)]//text()")
        all_paragraphs = all_paragraphs_r.extract()
        article_authors = response.xpath('//a[@rel="author"]/@href').extract()
        article_tags = response.xpath("//p[contains(@class, 'categories')]/a/@href").extract()
        article_date_str = response.xpath("//span[@class='date']//text()").extract_first()

        article_date = get_date_from_string(article_date_str)

        all_paragraph_text = build_text_from_paragraphs(all_paragraphs, punct_add_point=")")

        if (end_condition(article_date,  self.go_back_date)):
            self.finished = True
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : article_tags}

