# -*- coding: utf-8 -*-
import logging

import scrapy
from scrapy import Request

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled

from . import TechControversySpider
class EngadgetSpider(TechControversySpider):
    name = "engadget"
    pages_C =  0
    urls_V = set()
    pages_V = set()
    allowed_domains = ["engadget.com"]
    start_urls = (
        'https://www.engadget.com/', 'http://www.engadget.com/'
    )



    def __init__(self, article_repo, go_back_date, url_list=None):
        super().__init__(article_repo, go_back_date, url_list)

    def get_next_page(self):
        return 'https://www.engadget.com/all/page/'+str(self.pages_C)

    def parse_crawl(self, response):
        urls = response.xpath('//h2[contains(@class,"mt-10@tp+")]/a/@href | //div[contains(@class,"container@m")]/article[contains(@class,"o-hit")]/a/@href').extract()
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

        if self.crawl_allowed():
            yield self.request_for_next_page()


    def parse_page(self, response):
        url = response.meta.get('URL')

        article_title_parts = response.xpath("//h1[contains(@class, 't-h4@m-')]//text()").extract()
        article_title = "".join(article_title_parts ).strip()
        all_paragraph_before = response.xpath("//div[contains(@class, 't-d7@m-')]//text()").extract()
        all_paragraphs = response.xpath(
            "//div[contains(@class, 'article-text')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()


        all_paragraph_text = build_text_from_paragraphs(all_paragraph_before + all_paragraphs)

        article_date = extract_date( url)

        if (end_condition(article_date, self.go_back_date)):

            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": [], "date" :article_date, "filename" : "", "tags" : []}


