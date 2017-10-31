# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from . import extract_date, end_condition, build_text_from_paragraphs


class TechcrunchSpider(scrapy.Spider):
    name = "techcrunch"
    pages_V = set()
    urls_V = set()
    allowed_domains = ["techcrunch.com"]
    start_urls = (
        'https://techcrunch.com/','http://techcrunch.com/'
    )

    def __init__(self, article_repo):
        super().__init__()
        self.article_repo = article_repo
        self.finished = False


    def parse(self, response):
        urls = response.xpath('//h2[@class="post-title"]/a/@href').extract()

        pages = response.xpath('//li[@class="next"]/a/@href').extract()

        for url in urls:

            absolute_url = response.urljoin(url)
            if (absolute_url not in self.urls_V):
                self.urls_V.add(absolute_url)

                yield Request(absolute_url, callback=self.parse_page,
                              meta={'URL': absolute_url})



        if not self.finished:
            for page in pages:
                absolute_page = response.urljoin(page)
                if (absolute_page not in self.pages_V):
                    self.pages_V.add(absolute_page)
                    yield Request(absolute_page , callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        article_title_parts = response.xpath('//h1[@class="alpha tweet-title"]//text()').extract()
        article_title = "".join(article_title_parts)
        all_paragraphs_r = response.xpath(
            "//div[contains(@class, 'article-entry')]//p[not(.//aside) and not(.//twitterwidget) and not(.//figure)]//text()")
        all_paragraphs = all_paragraphs_r.extract()
        article_authors = response.xpath('//a[@rel="author"]/@href').extract()
        article_tags = response.xpath("//div[contains(@class, 'loaded') or @class='tag-item']/a/@href").extract()


        article_date = extract_date( url)
        all_paragraph_text = build_text_from_paragraphs(all_paragraphs)

        if (end_condition(article_date)):
            self.finished = True
        yield {"title": article_title, "url" : url,  "text": all_paragraph_text, "authors": article_authors, "date" :article_date, "filename" : "", "tags" : article_tags}

