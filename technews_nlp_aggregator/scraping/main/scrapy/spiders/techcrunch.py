# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging
import json
from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled


class TechcrunchSpider(scrapy.Spider):
    name = "techcrunch"
    pages_V = set()
    pages_C = 0
    urls_V = set()
    allowed_domains = ["techcrunch.com"]
    start_urls = (
        'https://techcrunch.com/', 'http://techcrunch.com/'
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
            if response.headers['Content-Type'] == b'application/json; charset=UTF-8':
                jsonresponse = json.loads(response.body_as_unicode())

                urls = [obj["link"] for obj in jsonresponse]
                for url in urls:

                    absolute_url = response.urljoin(url)
                    if (absolute_url not in self.urls_V and not already_crawled(self.article_repo, absolute_url) ):
                        self.urls_V.add(absolute_url)

                        yield Request(absolute_url, callback=self.parse_page,
                                      meta={'URL': absolute_url})
                    else:
                        article_date = self.article_repo.url_date(absolute_url)
                        if (end_condition(article_date, self.go_back_date)):
                            logging.info("Found article at date {}, finishing crawling".format(article_date))
                            self.finished += 1

            if self.finished < 5 and self.pages_C < 200:
                absolute_page =  'https://techcrunch.com/wp-json/tc/v1/magazine?page='+str(self.pages_C)
                self.pages_C += 1

                logging.info("Adding absolute page " + absolute_page)
                if (absolute_page not in self.pages_V):
                    self.pages_V.add(absolute_page)

                    yield Request(absolute_page, callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@class="article__title"]//text()').extract()
        article_title = "".join(article_title_parts)

        all_paragraphs_r = response.xpath(
            "//div[contains(@class, 'article-content')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//script) and not(.//div[contains(@class, 'fb_post')])]//text()")
        all_paragraphs = all_paragraphs_r.extract()



        article_date = extract_date( url)
        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)

        if (end_condition(article_date, self.go_back_date)):
            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": [], "date" :article_date, "filename" : "", "tags" : []}

