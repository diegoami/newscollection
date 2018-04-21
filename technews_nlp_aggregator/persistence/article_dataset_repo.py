import logging
import traceback

import dataset
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

from technews_nlp_aggregator.common.util import extract_date, extract_last_part, extract_host, remove_emojis, \
    extract_normpath, extract_source_without_www
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer


class ArticleDatasetRepo():

    def get_connection(self):
        return self.dataset_connection

    def __init__(self, db_connection, limit_article_id=None):
        self.db_connection = db_connection

        self.con_find = None
        self.dataset_connection = dataset.connect(self.db_connection, engine_kwargs={
            'connect_args': {'charset': 'utf8'}
        })
        self.engine = self.dataset_connection.engine


    def init_con_find(self):
        self.con_find = self.get_connection()

    def url_exists(self, url):
        if not self.con_find:
            self.init_con_find()
        found_one =  self.con_find['ARTICLE_INFO'].find_one(AIN_URL=url)

        result = found_one is not None
        return result

    def url_date(self, url):
        if not self.con_find:
            self.init_con_find()
        found_date =  self.con_find['ARTICLE_INFO'].find_one(AIN_URL=url)
        if found_date is not None:
            result = found_date['AIN_DATE']
        else:
            return None

    def close_con_find(self):
        self.con_find = None

    def get_latest_article_date(self):
        max_date_sql = "SELECT MAX(AIN_DATE) AS MAX_AIN_DATE FROM ARTICLE_INFO"
        con = self.get_connection()
        max_date_query = con.query(max_date_sql)
        max_date = next(max_date_query, None)
        return max_date["MAX_AIN_DATE"]


    def update_article(self, to_add):
        result = False
        if not "date" in to_add:
            to_add["date"] = extract_date(to_add["url"])
        source = extract_host(to_add["url"])
        norm_url = extract_normpath(to_add["url"])
        con = self.get_connection()
        try:

            con.begin()
            row = con['ARTICLE_INFO'].find_one(AIN_URL=norm_url )
            if row:
                pk = row["AIN_ID"]
                new_title = remove_emojis(to_add["title"])
                print("Updating {} to title {}".format(pk, new_title))

                pk = con['ARTICLE_INFO'].update(
                    dict({
                        "AIN_ID": pk,
                        "AIN_URL" : norm_url ,
                        "AIN_DATE" : to_add["date"],
                        "AIN_TITLE" : new_title,
                        "AIN_FILENAME": to_add["filename"]
                    }),['AIN_ID']
                )
                result = True
            con.commit()

        except:
            traceback.print_exc()
            con.rollback()

        return result

    def update_article_text(self,  article_id, new_text, con = None ):
        result = False
        try:
            con = self.get_connection() if not con else con

            con.begin()
            row = con['ARTICLE_TEXT'].find_one(ATX_AIN_ID=article_id)
            if row:
                pk = row["ATX_ID"]
                cleaned_text = defaultTokenizer.clean_text(new_text)
                logging.debug(cleaned_text)
                pk = con['ARTICLE_TEXT'].update(
                    dict({
                        "ATX_ID": pk,
                        "ATX_AIN_ID" : article_id,
                        "ATX_TEXT": cleaned_text,
                        "ATX_TEXT_ORIG": new_text
                    }),['ATX_ID']
                )
                result = True
            con.commit()

        except:
            traceback.print_exc()
            con.rollback()

        return result


    def save_article(self, to_add, text):
        if not "date" in to_add:
            to_add["date"] = extract_date(to_add["url"])
        text = remove_emojis(text)
        cleaned_text = defaultTokenizer.clean_text(text)
        pk = None
        if (len(cleaned_text) < 600):
            return None

        source = extract_host(to_add["url"])
        norm_url = extract_normpath(to_add["url"])
        found = False
        con = self.get_connection()
        try:

            con.begin()

            row = con['ARTICLE_INFO'].find_one(AIN_URL=norm_url )
            if not row:
                pk = con['ARTICLE_INFO'].insert(
                    dict({
                        "AIN_URL" : norm_url ,
                        "AIN_DATE" : to_add["date"],
                        "AIN_TITLE" : remove_emojis(to_add["title"]),
                        "AIN_FILENAME": to_add.get("filename","")
                    })
                )
            else:
                pk = row["AIN_ID"]
                found = True
            if (pk):
                if not con['ARTICLE_TEXT'].find_one(ATX_AIN_ID=str(pk)):
                    logging.info("Trying to write article at "+str(pk))
                    con['ARTICLE_TEXT'].insert(
                        dict({
                            "ATX_AIN_ID": pk,
                            "ATX_TEXT": cleaned_text,
                            "ATX_TEXT_ORIG": text
                        })

                    )
            authors = to_add.get("authors",[])
            for author in authors:
                if ("http" not in author):
                    author = source+author

                author_row = con['AUTHORS'].find_one(AUT_URL=author)
                if not author_row:
                    author_pk = con['AUTHORS'].insert(
                        dict({
                            "AUT_NAME": extract_last_part(author),
                            "AUT_URL":   author,

                        })
                    )
                else:
                    author_pk = author_row["AUT_ID"]
                if (author_pk and pk):
                    if not con['ARTICLE_AUTHORS'].find_one(
                            AAU_AIN_ID=str(pk), AAU_AUT_ID=str(author_pk)):
                        con['ARTICLE_AUTHORS'].insert(
                            dict({
                                "AAU_AIN_ID": pk,
                                "AAU_AUT_ID": author_pk
                            })

                        )
            tags = to_add.get("tags",[])
            for tag in tags:
                tag_row = con['TAGS'].find_one(TAG_URL=tag)
                if not tag_row:
                    tag_pk = con['TAGS'].insert(
                        dict({
                            "TAG_NAME": extract_last_part(tag),
                            "TAG_URL": tag,

                        })
                    )
                else:
                    tag_pk = tag_row["TAG_ID"]
                if (tag_pk and pk):
                    if not con['ARTICLE_TAGS'].find_one(
                            ATA_AIN_ID=str(pk), ATA_TAG_ID=str(tag_pk)):
                        con['ARTICLE_TAGS'].insert(
                            dict({
                                "ATA_AIN_ID": pk,
                                "ATA_TAG_ID": tag_pk
                            })

                        )
            con.commit()
        except:
            traceback.print_exc()
            con.rollback()

        return pk




    def load_articles(self, load_text=True, load_only_unsaved=True):
        econ=self.engine.connect()
        where_string = (" AND AIN_SAVED IS NULL ") if load_only_unsaved else ""
        if (load_text):
            article_info_sql= "SELECT AIN_ID, AIN_URL , AIN_TITLE, AIN_DATE, ATX_TEXT, AIN_PROCESSED FROM ARTICLE_INFO, ARTICLE_TEXT WHERE ATX_AIN_ID = AIN_ID "+where_string+ " ORDER BY AIN_ID"

        else:
            article_info_sql = "SELECT AIN_ID, AIN_URL , AIN_TITLE, AIN_DATE FROM ARTICLE_INFO WHERE 1 = 1 " + where_string + " ORDER BY AIN_ID"
        articleDF = pd.read_sql(article_info_sql,  econ)
        if (load_text):
            articleDF.columns = ['article_id' , 'url', 'title', 'date_p', 'text' , 'processed']

        else:
            articleDF.columns = ['article_id', 'url', 'title', 'date_p']
        econ.close()
        return articleDF



    def load_articles_with_text(self, id1, id2):
        con = self.get_connection()
        article1 = self.load_article_with_text(id1, con)
        article2 = self.load_article_with_text(id2, con)
        return article1, article2


    def load_articles_for_process(self):
        econ=self.engine.connect()
        article_process_sql = "SELECT @curRow := @curRow + 1 AS AIN_ROW, AIN_ID, AIN_DATE FROM ARTICLE_INFO IL JOIN (SELECT @curRow := 0) R WHERE AIN_PROCESSED IS NULL"

        articlesProcessDF = pd.read_sql(article_process_sql ,  econ, index_col="AIN_ROW")
        return articlesProcessDF

    def load_article_with_text(self, id, con=None):
        article_info_sql = "SELECT AIN_ID, AIN_URL, AIN_TITLE, AIN_DATE, ATX_TEXT FROM ARTICLE_INFO, ARTICLE_TEXT WHERE ATX_AIN_ID = AIN_ID AND AIN_ID = :id"
        con = self.get_connection() if not con else con
        article_query = con.query(article_info_sql, {"id": id})
        article = next(article_query , None)
        article["SOURCE"] = extract_source_without_www(article["AIN_URL"] )
        if article:
            return article
        else:
            return None

    def load_tags_tables(self):
        econ = self.engine.connect()
        where_string = (" WHERE ATA_AIN_ID <= " + str(self.limit_article_id)) if self.limit_article_id else ""
        tags_sql = "SELECT TAG_ID, TAG_NAME, TAG_URL FROM TAGS"
        tags_articles_sql = "SELECT ATA_ID, ATA_AIN_ID, ATA_TAG_ID FROM ARTICLE_TAGS" +  where_string

        tagsDF = pd.read_sql(tags_sql , econ)
        tagsDF.columns = ['tag_id', 'name', 'url']
        articleTagsDF = pd.read_sql(tags_articles_sql, econ)
        articleTagsDF.columns = ['tag_article_id', 'article_id', 'tag_id']

        econ.close()
        return tagsDF, articleTagsDF


    def delete_unrelevant_texts(self):
        session = create_session()
        connection = self.engine.raw_connection()
        cursor = connection.cursor()
        cursor.callproc("detect_uninteresting")
        cursor.close()
        connection.commit()
        cursor = connection.cursor()
        cursor.callproc("delete_ids")
        cursor.close()
        connection.commit()

    def update_to_saved(self,  con=None):
        sql_update = "UPDATE ARTICLE_INFO SET AIN_SAVED = SYSDATE()"
        con = self.get_connection() if not con else con
        try:
            con.begin()
            article_query = con.query(sql_update)
            con.commit()
        except:
            con.rollback()
            traceback.print_stack()

    def update_to_crawled(self, url, con=None):
        sql_update = "UPDATE URLS_TO_ADD SET UTA_PROCESSED = SYSDATE() WHERE UTA_URL LIKE :url"
        con = self.get_connection() if not con else con
        try:
            con.begin()
            article_query = con.query(sql_update, {"url" : '%'+url.strip()+'%'})
            con.commit()
        except:
            con.rollback()
            traceback.print_stack()

    def load_articles_containing(self, text_to_search, page_id, n_articles, start_s=None, end_s=None):
        offset = page_id  * n_articles
        article_query_sql = "SELECT AIN_ID, AIN_URL, AIN_TITLE, AIN_DATE FROM ARTICLE_INFO, ARTICLE_TEXT WHERE ATX_AIN_ID = AIN_ID "+\
                            (start_s and ( " AND AIN_DATE >= '" + start_s + "' " )) + \
                            (end_s and ( " AND AIN_DATE <= '" + end_s + "' ")) + \
                            " AND (AIN_TITLE LIKE '%%"+text_to_search+"%%' OR ATX_TEXT LIKE '%%"+text_to_search+"%%') ORDER BY AIN_ID DESC LIMIT " + str(offset) + "," + str(n_articles)
        econ = self.engine.connect()
        articlesFoundDF = pd.read_sql(article_query_sql, econ, index_col=None)
        articlesFoundDF["SOURCE"] = articlesFoundDF['AIN_URL'].map(extract_source_without_www)
        econ.close()
        return articlesFoundDF