# -*- coding: utf-8 -*-

from . import end_condition, build_text_from_paragraphs, build_from_timestamp

from . import TechControversySpider
class CnbcSpider(TechControversySpider):
    name = "cnbc"
    finished = 0
    pages_C = 0
    skipped = 0

    urls_V = set()
    pages_V = set()
    allowed_domains = ["cnbc.com"]
    start_urls = (
        'https://www.cnbc.com/', 'http://www.cnbc.com/'   )

    def __init__(self, article_repo, go_back_date, url_list):
        super().__init__(article_repo, go_back_date, url_list)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@class="title"]//text()').extract()
        article_title = "".join(article_title_parts).strip()
        all_paragraph_before = response.xpath("//div[@id='article_deck']//li/text()").extract()
        all_paragraphs = response.xpath(
            "//div[contains(@class, 'group-container')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure) and not(.//h2)  and not(.//script) and not(.//div[@class=mid-banner-wrap])]//text()").extract()

        article_authors = response.xpath('//a[@rel="author"]/@href').extract_first()
        all_paragraph_text = build_text_from_paragraphs( all_paragraph_before + all_paragraphs)
        article_datetime_ts = response.xpath('//time/@datetime').extract_first()
        article_date = build_from_timestamp(article_datetime_ts)
        if (end_condition(article_date, self.go_back_date)):
            self.finished += 1
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : []}


