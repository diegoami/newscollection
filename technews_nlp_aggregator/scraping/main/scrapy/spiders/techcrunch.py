# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging
import json
from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled

from . import TechControversySpider
class TechcrunchSpider(TechControversySpider):
    name = "techcrunch"
    pages_V = set()
    pages_C = 0
    urls_V = set()
    allowed_domains = ["techcrunch.com"]
    start_urls = (
        'https://techcrunch.com/', 'http://techcrunch.com/'
    )

    def __init__(self, article_repo, go_back_date, url_list=None):
        super().__init__(article_repo, go_back_date, url_list)

    def get_next_page(self):
        return 'https://techcrunch.com/wp-json/tc/v1/magazine?page='+str(self.pages_C)

    def parse(self, response):
        super().parse(response)
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
                    else:
                        self.skipped += 1

        if self.crawl_allowed():
            yield self.request_for_next_page()

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@class="article__title"]//text()').extract()
        article_title = "".join(article_title_parts)

        all_paragraphs_r = response.xpath(
            "//div[contains(@class, 'article-content')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//script) and not(.//div[contains(@class, 'fb_post')])]//text()")
        all_paragraphs = all_paragraphs_r.extract()



        article_date = extract_date(url)
        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)

        if (end_condition(article_date, self.go_back_date)):
            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": [], "date" :article_date, "filename" : "", "tags" : []}

