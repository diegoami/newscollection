import logging
import traceback

import dataset
from sqlalchemy import create_engine

from technews_nlp_aggregator.common.util import extract_date, extract_last_part, extract_host, remove_emojis
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import pandas as pd


class ArticleDatasetRepo():
    tags_query = 'SELECT TAG_NAME, TAG_URL FROM ARTICLE_INFO, ARTICLE_TAGS, TAGS WHERE TAG_ID = ATA_TAG_ID AND ATA_AIN_ID = AIN_ID AND AIN_ID = :id'
    authors_query = 'SELECT AUT_NAME, AUT_URL FROM ARTICLE_INFO, ARTICLE_AUTHORS, AUTHORS WHERE AAU_AIN_ID = AIN_ID AND AUT_ID = AAU_AUT_ID AND AIN_ID = :id'

    def get_connection(self):
        con = dataset.connect(self.db_connection, engine_kwargs={
            'connect_args': {'charset': 'utf8'}
        })
        return con

    def __init__(self, db_connection, limit_article_id=None):
        self.db_connection = db_connection
        self.limit_article_id = limit_article_id

        self.engine = create_engine(self.db_connection,encoding='UTF-8')


    def init_con_find(self):
        self.con_find = self.get_connection()

    def url_exists(self, url):
        if self.con_find == None:
            self.init_con_find()
        found_one =  self.con_find['ARTICLE_INFO'].find_one(AIN_URL=url)

        result = found_one is not None
        return result

    def close_con_find(self):
        self.con_find = None

    def file_name_exists(self, filename):
        row = self.get_connection()['ARTICLE_INFO'].find_one(AIN_FILENAME=filename)
        if row:
            pk = row["AIN_ID"]
            return self.get_connection()['ARTICLE_TEXT'].find_one(ATX_AIN_ID=pk)
        else:
            return False


    def update_article(self, url, to_add):
        result = False
        if not "date" in to_add:
            to_add["date"] = extract_date(to_add["url"])
        source = extract_host(url)
        try:
            con = self.get_connection()
            con.begin()
            row = con['ARTICLE_INFO'].find_one(AIN_URL=to_add["url"])
            if row:
                pk = row["AIN_ID"]
                new_title = remove_emojis(to_add["title"])
                print("Updating {} to title {}".format(pk, new_title))

                pk = con['ARTICLE_INFO'].update(
                    dict({
                        "AIN_ID": pk,
                        "AIN_URL" : to_add["url"],
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

    def update_article_text(self,  article_id, new_text, con = None, ):
        result = False
        try:
            con = self.get_connection() if not con else con
            con.begin()
            row = con['ARTICLE_TEXT'].find_one(ATX_AIN_ID=article_id)
            if row:
                pk = row["ATX_ID"]

                pk = con['ARTICLE_TEXT'].update(
                    dict({
                        "ATX_ID": pk,
                        "ATX_AIN_ID" : article_id,
                        "ATX_TEXT": defaultTokenizer.clean_text(new_text),
                        "ATX_TEXT_ORIG": new_text
                    }),['ATX_ID']
                )
                result = True
            con.commit()

        except:
            traceback.print_exc()
            con.rollback()

        return result


    def save_article(self, url, to_add, text):
        if not "date" in to_add:
            to_add["date"] = extract_date(to_add["url"])
        source = extract_host(url)
        found = False
        try:
            con = self.get_connection()
            con.begin()

            row = con['ARTICLE_INFO'].find_one(AIN_URL=to_add["url"])
            if not row:
                pk = con['ARTICLE_INFO'].insert(
                    dict({
                        "AIN_URL" : to_add["url"],
                        "AIN_DATE" : to_add["date"],
                        "AIN_TITLE" : remove_emojis(to_add["title"]),
                        "AIN_FILENAME": to_add["filename"]
                    })
                )
            else:
                pk = row["AIN_ID"]
                found = True
            if (pk):
                if not con['ARTICLE_TEXT'].find_one(ATX_AIN_ID=str(pk)):
                    text = remove_emojis(text)
                    print("Trying to write article at "+str(pk))
                    con['ARTICLE_TEXT'].insert(
                        dict({
                            "ATX_AIN_ID": pk,
                            "ATX_TEXT": defaultTokenizer.clean_text(text),
                            "ATX_TEXT_ORIG": text
                        })

                    )
            authors = to_add["authors"]
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
            tags = to_add["tags"]
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

        return found




    def load_articles(self):
        econ=self.engine.connect()
        where_string = (" AND AIN_ID <= "+str(self.limit_article_id)) if self.limit_article_id else ""
        article_info_sql= "SELECT AIN_ID, AIN_URL , AIN_TITLE, AIN_DATE, ATX_TEXT FROM ARTICLE_INFO, ARTICLE_TEXT WHERE ATX_AIN_ID = AIN_ID "+where_string+ " ORDER BY AIN_ID"

        articleDF = pd.read_sql(article_info_sql,  econ)
        articleDF.columns = ['article_id' , 'url', 'title', 'date_p', 'text' ]

        econ.close()
        return articleDF

    def load_articles_with_text(self, id1, id2):
        con = self.get_connection()
        article1 = self.load_article_with_text(id1, con)
        article2 = self.load_article_with_text(id2, con)
        return article1, article2

    def load_article_with_text(self, id, con=None):
        article_info_sql = "SELECT AIN_ID, AIN_URL, AIN_TITLE, AIN_DATE, ATX_TEXT, ATX_TEXT_ORIG FROM ARTICLE_INFO, ARTICLE_TEXT WHERE ATX_AIN_ID = AIN_ID AND AIN_ID = :id"
        con = self.get_connection() if not con else con
        article_query = con.query(article_info_sql, {"id": id})
        article = next(article_query , None)
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


    def load_authors_tables(self):
        econ = self.engine.connect()
        where_string = (" WHERE AAU_AIN_ID <= " + str(self.limit_article_id)) if self.limit_article_id else ""
        authors_sql = "SELECT AUT_ID, AUT_NAME, AUT_URL FROM AUTHORS"
        authors_articles_sql = "SELECT AAU_ID, AAU_AIN_ID, AAU_AUT_ID FROM ARTICLE_AUTHORS"

        authorsDF = pd.read_sql(authors_sql, econ)
        authorsDF.columns = ['author_id', 'name', 'url']
        articleAuthorsDF = pd.read_sql(authors_articles_sql, econ)
        articleAuthorsDF.columns = ['author_article_id', 'article_id', 'author_id']

        econ.close()
        return authorsDF, articleAuthorsDF


    def retrieve_tags_authors(self, article_id):
        tags, authors = [], []
        con = self.get_connection()
        for tag_row in con.query(self.tags_query, id=article_id):
            tags.append({"url": tag_row["TAG_URL"], "name": tag_row["TAG_NAME"]})
        for author_row in con.query(self.authors_query, id=article_id):
            authors.append({"url": author_row["AUT_URL"], "name": author_row["AUT_NAME"]})

        return tags, authors


    def delete_short_texts(self):

        con = self.get_connection()
        try:
            con.begin()
            con.query('CALL detect_short_txts()')
            con.commit()
        except:
            con.rollback()
        try:
            con.begin()
            con.query('CALL delete_ids()')
            con.commit()
        except:
            con.rollback()


"""
 def load_text(self, article_sub_DF, load_text=True):
        econ = self.engine.connect()
        if "text" not in article_sub_DF.columns:
            articleids = article_sub_DF.index
            where_string = (" WHERE ATX_AIN_ID <= " + str(self.limit_article_id)) if self.limit_article_id else ""
            if (load_text):
                article_text_sql = 'SELECT ATX_ID, ATX_TEXT, ATX_AIN_ID FROM ARTICLE_TEXT  '+where_string
            else:
                article_text_sql = 'SELECT ATX_ID, \'\', ATX_AIN_ID FROM ARTICLE_TEXT  ' +where_string
            articleTextDF = pd.read_sql(article_text_sql , econ, index_col='ATX_ID')
            articleTextDF.columns = [ 'text', 'article_id' ]

            article_sub_DF = article_sub_DF.merge(articleTextDF, on='article_id')

        econ.close()
        return article_sub_DF
"""