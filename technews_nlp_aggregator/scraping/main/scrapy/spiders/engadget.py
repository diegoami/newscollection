# -*- coding: utf-8 -*-
import logging

import scrapy
from scrapy import Request

from . import extract_date, end_condition, build_text_from_paragraphs, already_crawled

from scrapy.spiders import Spider
from scrapy.http import Request, XmlResponse
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots
from scrapy.utils.gz import gunzip, gzip_magic_number
from scrapy.spiders.sitemap import iterloc

logger = logging.getLogger(__name__)


from . import TechControversySpider
class EngadgetSpider(scrapy.spiders.SitemapSpider):
    name = "engadget"
    finished = 0
    pages_C = 0
    skipped = 0

    allowed_domains = ["engadget.com"]
    start_urls = ['https://www.engadget.com']
    sitemap_urls = ['https://www.engadget.com/sitemap-posts1.xml.gz']



    def __init__(self, article_repo, go_back_date, url_list=None):
        super().__init__()
        self.article_repo = article_repo
        self.go_back_date = go_back_date
        self.url_list = url_list



    def start_requests(self):
        for url in self.sitemap_urls:
            yield Request(url,  meta={'dont_redirect': True,"handle_httpstatus_list": [302, 307]}, callback=self._parse_sitemap)

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

    def _parse_sitemap(self, response):

        body = self._get_sitemap_body(response)
        if body is None:
            logger.warning("Ignoring invalid sitemap: %(response)s",
                           {'response': response}, extra={'spider': self})
            return

        s = Sitemap(body)
        for loc in iterloc(s, self.sitemap_alternate_links):
            for r, c in self._cbs:
                if r.search(loc):
                    article_date = extract_date(loc)
                    if not (end_condition(article_date, self.go_back_date)):
                        logging.info("Adding {}".format(loc))
                        yield Request(loc, meta={'URL': loc, 'dont_redirect': True,"handle_httpstatus_list": [302, 307]}, callback=self.parse_page)
                        break
