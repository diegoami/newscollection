from os.path import basename
from bs4 import BeautifulSoup
from . import url_to_filename, remove_query_part
from datetime import date, datetime
from technews_nlp_aggregator.persistence import ArticleDatasetRepo
from technews_nlp_aggregator.common import extract_date


import os
class Converter:

    def __init__(self,raw_base_dir, db_connection, iterator):

        self.iterator = iterator
        self.raw_base_dir = raw_base_dir
        self.article_repo = ArticleDatasetRepo(db_connection)

    def retrieve_title_and_text(self, article, braw_article):

        article_title, all_paragraph_text, article_date = None, None, None
        bs_article = BeautifulSoup(article)
        if (braw_article.startswith("techcrunch") or braw_article.startswith("jp_techcrunch")):
            article_entry = bs_article.find('div', {'class': 'article-entry'})
            article_title_t = bs_article.find('h1', {'class': 'alpha tweet-title'})
            article_tag_roots = bs_article.find_all('div', {'class': 'loaded acc-handle'})
            article_tags = self.retrieve_tags(article_tag_roots)
            article_authors = []
            article_authors_roots = bs_article.find_all('a', {'rel': 'author'})
            for article_authors_root in article_authors_roots:
                if article_authors_root.get('href'):
                    article_authors.append(article_authors_root["href"])
        elif (braw_article.startswith("thenextweb")):
            article_entry = bs_article.find('div', {'class': 'post-body'})
            article_title_t = bs_article.find('h1', {'class': 'u-m-0_25'})
            article_tag_roots = bs_article.find_all('span', {'class': 'tag'})
            article_tags = self.retrieve_tags(article_tag_roots)
            article_authors = []
            article_authors_roots = bs_article.find_all('a', {'class': 'post-authorName'})

            for article_authors_root in article_authors_roots:
                if article_authors_root.get('href'):
                    article_authors.append(article_authors_root["href"])
        elif (braw_article.startswith("www_theverge")):
            article_entry = bs_article.find('div', {'class': 'c-entry-content'})
            article_title_t = bs_article.find('h1', {'class': 'c-page-title'})
            article_tag_roots = bs_article.find_all('li', {'class': 'c-entry-group-labels__item'})
            article_tags = self.retrieve_tags(article_tag_roots)
            article_authors = []
            article_authors_hero = bs_article.find('div', {'class': 'c-entry-hero c-entry-hero--default'})
            if (article_authors_hero):
                article_authors_roots = article_authors_hero.find_all('span', {'class': 'c-byline__item'})
                for article_authors_root in article_authors_roots:
                    article_authors_as = article_authors_root.find_all('a')
                    for article_authors_a in article_authors_as:
                        if article_authors_a.get('href'):
                            if ('/users/' in article_authors_a["href"]):
                                article_authors.append(article_authors_a["href"])
        elif (braw_article.startswith("venturebeat_com")):
            article_entry = bs_article.find('div', {'class': 'article-content'})
            article_title_t = bs_article.find('h1', {'class': 'article-title'})
            article_tags_roots = bs_article.find_all('a', {'class': 'article-category'})
            article_tags = []
            for article_tags_root in article_tags_roots :
                href = article_tags_root['href']
                article_tags.append(href)

            article_authors = []
            article_authors_hero = bs_article.find('div', {'class': 'article-byline'})
            if (article_authors_hero):
                article_authors_roots = article_authors_hero.find_all('a', {'rel': 'author'})
                for article_authors_root in article_authors_roots:
                    if article_authors_root.get('href'):
                        article_authors.append(article_authors_root["href"])
        elif (braw_article.startswith("arstechnica_com")):
            article_entry = bs_article.find('div', {'itemprop': 'articleBody'})
            article_title_t = bs_article.find('h1', {'itemprop': 'headline'})

            article_tags = []
            article_authors = []
            article_authors_roots = bs_article.find_all('a', {'rel': 'author'})
            for article_authors_root in article_authors_roots:
                if article_authors_root.get('href'):
                    article_authors.append(article_authors_root["href"])
            article_date_root = bs_article.find('time')

            article_datetime_tsstring = article_date_root.get('datetime')
            article_date_str = article_datetime_tsstring.split('T')[0]
            article_date = datetime.strptime(article_date_str,'YYYY-MM-DD')

        if (article_title_t and article_entry):
            all_paragraphs = bs_article.find_all('p')
            all_paragraph_text = "\n".join(
                [x.text for x in all_paragraphs if len(x.text) > 0 and not x.text[0] == '\n'])
            article_title = article_title_t.text

        return {"title": article_title, "text": all_paragraph_text, "tags": article_tags, "authors": article_authors, "date" :article_date}

    def retrieve_tags(self, article_tag_roots):
        tags = []
        for article_tag_root in article_tag_roots:
            internal_a = article_tag_root.find('a')
            if internal_a:
                href = internal_a['href']
                tags.append(href)
        return tags

    def convert_articles(self, stopat=None, showEntry = False):
        count = 0
        for lurl, v in self.iterator:
            url = remove_query_part(lurl)

            braw_article = url_to_filename(url)
            lbraw_article = url_to_filename(lurl)
            raw_article = self.raw_base_dir + braw_article
            lraw_article = self.raw_base_dir + lbraw_article
            filename = braw_article + '.txt'

            link_file_exists = self.article_repo.url_exists(url)
            if (not os.path.isfile(raw_article)):
                raw_article = lraw_article

            if (os.path.isfile(raw_article)):

                if (self.article_repo.file_name_exists(filename) and link_file_exists):
                    continue
                with open(raw_article, 'r') as f:
                    article_full_text = f.read()
                    article = self.retrieve_title_and_text(article_full_text, braw_article)
                    if ("title" in article and "text" in article and article["title"] and article["text"] and len(
                                article["text"]) > 400):
#                        if (not self.article_repo.file_name_exists(filename) ):
 #                           self.article_repo.save_text_to_file(filename, article["title"], article["text"])
  #                      if (not link_file_exists):
                        article["filename"] = filename
                        article["date"] = extract_date( url) if not article.get("date") else article.get("date")
                        article["url"] = url
                        to_add = {k: v for k, v in article.items() if k != "text"}
                        self.article_repo.save_article(url, to_add, article["text"])
                        if (showEntry):
                            print(to_add)
                        if (count % 50) == 0:
                            self.article_repo.save_articles()
                            print("Saving ....")
                        count += 1
                        if (stopat and count > stopat):
                            break


            else:
                print("This file could not be found: " + raw_article)

            self.article_repo.save_articles()
