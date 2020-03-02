# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled




from . import TechControversySpider
class VenturebeatSpider(TechControversySpider):
    name = "venturebeat"
    finished = 0
    pages_C = 0
    skipped = 0

    urls_V = set()
    pages_V = set()
    allowed_domains = ["venturebeat.com"]
    start_urls = (
        'https://venturebeat.com/', 'http://venturebeat.com/'
    )


    def __init__(self, article_repo, go_back_date, url_list=None):
        super().__init__(article_repo, go_back_date, url_list)

    def get_next_page(self):
        return 'https://venturebeat.com/page/'+str(self.pages_C)

    def parse_crawl(self, response):
        urls = response.xpath('//h2[@class="ArticleListing__title"]/a/@href').extract()
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
        article_title_parts = response.xpath('//h1[@class="article-title"]//text()').extract()
        article_title = "".join(article_title_parts).strip()

        all_paragraphs = response.xpath(
            "//div[contains(@class, 'article-content')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//strong/script)]//text()").extract()
        article_authors = response.xpath('//div[@class="article-byline"]/a[@rel="author"]/@href').extract()
        article_tags = response.xpath("//a[contains(@class, 'article-category')]/@href").extract()

        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)


        article_date = extract_date(url)
        if (end_condition(article_date, self.go_back_date)):
            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : article_tags}


