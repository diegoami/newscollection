# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

import logging

from . import extract_date,  end_condition, build_text_from_paragraphs, already_crawled




class ThevergeSpider(scrapy.Spider):
    name = "theverge"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["theverge.com"]
    start_urls = (
        'https://www.theverge.com/', 'http://www.theverge.com/'
    )


    def __init__(self, article_repo, go_back_date, url_list=None):
        super().__init__()
        self.article_repo = article_repo
        self.go_back_date = go_back_date

        self.finished = 0
        self.url_list = url_list


    def parse(self, response):
        if self.url_list:
            for url in self.url_list:
                yield Request(url , callback=self.parse_page,
                          meta={'URL': url})
        else:


            urls = response.xpath('//h3/a/@href | //h2/a/@href').extract()


            for url in urls:

                absolute_url = response.urljoin(url)
                article_date = extract_date(url)
                if (article_date):
                    if (absolute_url not in self.urls_V and not already_crawled(self.article_repo, absolute_url)):
                        self.urls_V.add(absolute_url)

                        yield Request(absolute_url, callback=self.parse_page,
                                      meta={'URL': absolute_url})

                    else:
                        if (end_condition(article_date, self.go_back_date)):
                            logging.info("Found article at date {}, finishing crawling".format(article_date))
                            self.finished += 1
                        else:
                            self.skipped += 1
            if self.finished < 5 and self.pages_C < 200 and self.skipped < 500:
                absolute_page = 'https://www.theverge.com/archives/'+str(self.pages_C)
                self.pages_C += 1


                logging.info("Adding absolute page "+absolute_page )
                if (absolute_page not in self.pages_V):
                    self.pages_V.add(absolute_page)

                    yield Request(absolute_page , callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@class="c-page-title"]//text()').extract()
        article_title = "".join(article_title_parts).strip()

        all_paragraphs = response.xpath(
            "//div[contains(@class, 'c-entry-content')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(./div/twitterwidget)  and not(.//script) ]//text()").extract()
        article_authors = response.xpath('//div[@class="c-byline"]/span[@class="c-byline__item"]/a/@href').extract()
        article_tags = response.xpath("//li[contains(@class, 'c-entry-group-labels__item')]/a/@href").extract()

        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)


        article_date = extract_date(url)
        if (end_condition(article_date, self.go_back_date)):

            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : article_tags}

