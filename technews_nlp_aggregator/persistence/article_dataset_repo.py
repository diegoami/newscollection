from .article_repo import ArticleRepo

import dataset
from technews_nlp_aggregator.common.util import extract_date, extract_last_part, extract_host, remove_emojis
import sys, traceback

class ArticleDatasetRepo(ArticleRepo):
    tags_query = 'SELECT TAG_NAME, TAG_URL FROM ARTICLE_INFO, ARTICLE_TAGS, TAGS WHERE TAG_ID = ATA_TAG_ID AND ATA_AIN_ID = AIN_ID AND AIN_ID = :id'
    authors_query = 'SELECT AUT_NAME, AUT_URL FROM ARTICLE_INFO, ARTICLE_AUTHORS, AUTHORS WHERE AAU_AIN_ID = AIN_ID AND AUT_ID = AAU_AUT_ID AND AIN_ID = :id'

    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.db = dataset.connect(self.db_connection ,  engine_kwargs = {
            'connect_args' : {'charset' : 'utf8'}
        })

        self.article_info_tbl = self.db['ARTICLE_INFO']
        self.article_text_tbl = self.db['ARTICLE_TEXT']
        self.tags_tbl = self.db['TAGS']
        self.authors_tbl = self.db['AUTHORS']

        self.article_tags_tbl = self.db['ARTICLE_TAGS']
        self.article_authors_tbl = self.db['ARTICLE_AUTHORS']


    def extract_date(filename):
        arrs = filename.split('_')
        index = 0
        while not arrs[index].isdigit():
            index += 1
        year, month, day = arrs[index], arrs[index + 1], arrs[index + 2]
        date_str = day + '-' + month + '-' + year

        return date_str

    def url_exists(self, url):
        return self.article_info_tbl.find_one(AIN_URL=url)

    def file_name_exists(self, filename):
        row = self.article_info_tbl.find_one(AIN_FILENAME=filename)
        if row:
            pk = row["AIN_ID"]
            return self.article_text_tbl.find_one(ATX_AIN_ID=pk)
        else:
            return False

    def save_articles(self):
        self.db.commit()

    def save_article(self, url, to_add, text):
        if not "date" in to_add:
               to_add["date"] = extract_date(to_add["url"])
        source = extract_host(url)
        try:
            self.db.begin()

            row = self.article_info_tbl.find_one(AIN_URL=to_add["url"])
            if not row:
                pk = self.article_info_tbl.insert(
                    dict({
                        "AIN_URL" : to_add["url"],
                        "AIN_DATE" : to_add["date"],
                        "AIN_TITLE" : remove_emojis(to_add["title"]),
                        "AIN_FILENAME": to_add["filename"]
                    })
                )
            else:
                pk = row["AIN_ID"]
            if (pk):
                if not self.article_text_tbl.find_one(ATX_AIN_ID=str(pk)):
                    text = remove_emojis(text)
                    print("Trying to write article at "+str(pk))
                    self.article_text_tbl.insert(
                        dict({
                            "ATX_AIN_ID": pk,
                            "ATX_TEXT": text
                        })

                    )
            authors = to_add["authors"]
            for author in authors:
                if ("http" not in author):
                    author = source+author

                author_row = self.authors_tbl.find_one(AUT_URL=author)
                if not author_row:
                    author_pk = self.authors_tbl.insert(
                        dict({
                            "AUT_NAME": extract_last_part(author),
                            "AUT_URL":   author,

                        })
                    )
                else:
                    author_pk = author_row["AUT_ID"]
                if (author_pk and pk):
                    if not self.article_authors_tbl.find_one(
                            AAU_AIN_ID=str(pk), AAU_AUT_ID=str(author_pk)):
                        self.article_authors_tbl.insert(
                            dict({
                                "AAU_AIN_ID": pk,
                                "AAU_AUT_ID": author_pk
                            })

                        )
            tags = to_add["tags"]
            for tag in tags:
                tag_row = self.tags_tbl.find_one(TAG_URL=tag)
                if not tag_row:
                    tag_pk = self.tags_tbl.insert(
                        dict({
                            "TAG_NAME": extract_last_part(tag),
                            "TAG_URL": tag,

                        })
                    )
                else:
                    tag_pk = tag_row["TAG_ID"]
                if (tag_pk and pk):
                    if not self.article_tags_tbl.find_one(
                            ATA_AIN_ID=str(pk), ATA_TAG_ID=str(tag_pk)):
                        self.article_tags_tbl.insert(
                            dict({
                                "ATA_AIN_ID": pk,
                                "ATA_TAG_ID": tag_pk
                            })

                        )
            self.db.commit()
        except:
            traceback.print_exc()
            self.db.rollback()


    def flush(self):
        self.db.commit()


    def load_articles(self):
        article_info_rows = self.article_info_tbl.find(order_by=['AIN_DATE', 'AIN_TITLE'])
        article_records = []
        for article_info_row in article_info_rows:
            article_record = {
                "id"  :  article_info_row["AIN_ID"],
                "url" :  article_info_row["AIN_URL"],
                "date_p": article_info_row["AIN_DATE"],
                "title" : article_info_row["AIN_TITLE"]
            }
            article_record["date"] = article_record["date_p"].isoformat()
            id = article_record["id"]
            url = article_info_row["AIN_URL"]
            article_text_row = self.article_text_tbl.find_one(ATX_AIN_ID=id)
            article_record["text"] = article_text_row["ATX_TEXT"]
            article_record["tags"], article_record["tag_base"] = [], []
            for tag_row in self.db.query(self.tags_query,id=id):
                article_record["tags"].append(tag_row["TAG_URL"])
                article_record["tag_base"].append(tag_row["TAG_NAME"])
            article_record["authors"], article_record["author_base"] = [], []
            for author_row in self.db.query(self.authors_query, id=id):
                article_record["authors"].append(author_row["AUT_URL"])
                article_record["author_base"].append(author_row["AUT_NAME"])
            sourceindex = url.index(".com")
            article_record["source"] = url[:sourceindex]

            article_records.append(article_record)
        return article_records