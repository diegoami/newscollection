# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled





class VenturebeatSpider(scrapy.Spider):
    name = "venturebeat"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["venturebeat.com"]
    start_urls = (
        'https://venturebeat.com/', 'http://venturebeat.com/'
    )


    def __init__(self, article_repo, go_back_date, url_list):
        super().__init__()
        self.article_repo = article_repo
        self.go_back_date = go_back_date

        self.finished = False
        self.url_list = url_list


    def parse(self, response):
        if self.url_list:
            for url in self.url_list:
                yield Request(url, callback=self.parse_page,
                              meta={'URL': url})
        else:
            urls = response.xpath('//h2[@class="article-title"]/a/@href').extract()
            for url in urls:
                absolute_url = response.urljoin(url)
                article_date = extract_date(url)
                if (article_date):
                    if (absolute_url not in self.urls_V and not already_crawled(self.article_repo, absolute_url)):
                        self.urls_V.add(absolute_url)
                        yield Request(absolute_url, callback=self.parse_page,
                                      meta={'URL': absolute_url})



            if not self.finished:
                absolute_page = 'https://venturebeat.com/page/'+str(self.pages_C)
                self.pages_C += 1


                logging.info("Adding absolute page "+absolute_page )
                if (absolute_page not in self.pages_V):
                    self.pages_V.add(absolute_page)

                    yield Request(absolute_page , callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@class="article-title"]//text()').extract()
        article_title = "".join(article_title_parts).strip()

        all_paragraphs = response.xpath(
            "//div[contains(@class, 'article-content')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//strong/script)]//text()").extract()
        article_authors = response.xpath('//div[@class="article-byline"]/a[@rel="author"]/@href').extract()
        article_tags = response.xpath("//a[contains(@class, 'article-category')]/@href").extract()

        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)


        article_date = extract_date(url)
        if (end_condition(article_date, self.go_back_date)):

            self.finished = True
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : article_tags}


