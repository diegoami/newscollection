import logging
import traceback

import dataset
from sqlalchemy import create_engine

from technews_nlp_aggregator.common.util import extract_date, extract_last_part, extract_host, remove_emojis
from todiscard.json.article_repo import ArticleRepo

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import pandas as pd
from technews_nlp_aggregator.nlp_model.common import TechArticlesSentenceTokenizer

class ArticleDatasetRepo(ArticleRepo):
    tags_query = 'SELECT TAG_NAME, TAG_URL FROM ARTICLE_INFO, ARTICLE_TAGS, TAGS WHERE TAG_ID = ATA_TAG_ID AND ATA_AIN_ID = AIN_ID AND AIN_ID = :id'
    authors_query = 'SELECT AUT_NAME, AUT_URL FROM ARTICLE_INFO, ARTICLE_AUTHORS, AUTHORS WHERE AAU_AIN_ID = AIN_ID AND AUT_ID = AAU_AUT_ID AND AIN_ID = :id'

    def get_connection(self):
        con = dataset.connect(self.db_connection, engine_kwargs={
            'connect_args': {'charset': 'utf8'}
        })
        return con

    def __init__(self, db_connection):
        self.db_connection = db_connection

       # self.article_info_tbl = self.db['ARTICLE_INFO']
        #self.article_text_tbl = self.db['ARTICLE_TEXT']
       # self.tags_tbl = self.db['TAGS']
       # self.authors_tbl = self.db['AUTHORS']

       # self.article_tags_tbl = self.db['ARTICLE_TAGS']
       # self.article_authors_tbl = self.db['ARTICLE_AUTHORS']
        self.engine = create_engine(self.db_connection,encoding='UTF-8')
        self.sentence_tokenizer = TechArticlesSentenceTokenizer()

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



    def save_article(self, url, to_add, text):
        if not "date" in to_add:
            to_add["date"] = extract_date(to_add["url"])
        source = extract_host(url)
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
            if (pk):
                if not con['ARTICLE_TEXT'].find_one(ATX_AIN_ID=str(pk)):
                    text = remove_emojis(text)
                    print("Trying to write article at "+str(pk))
                    con['ARTICLE_TEXT'].insert(
                        dict({
                            "ATX_AIN_ID": pk,
                            "ATX_TEXT": text
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



    def load_text(self, article_sub_DF, all=False,load_text=True):
        econ = self.engine.connect()
        if "text" not in article_sub_DF.columns:
            articleids = article_sub_DF.index
            if (load_text):
                article_text_sql = 'SELECT ATX_ID, ATX_TEXT, ATX_AIN_ID FROM ARTICLE_TEXT  '+ ( ('WHERE ATX_AIN_ID IN '+str(tuple(articleids))) if not all else '')
            else:
                article_text_sql = 'SELECT ATX_ID, \'\', ATX_AIN_ID FROM ARTICLE_TEXT  ' + (
                ('WHERE ATX_AIN_ID IN ' + str(tuple(articleids))) if not all else '')
            articleTextDF = pd.read_sql(article_text_sql , econ, index_col='ATX_ID')
            articleTextDF.columns = [ 'text', 'article_id' ]

            article_sub_DF = article_sub_DF.merge(articleTextDF, on='article_id')

        econ.close()
        return article_sub_DF


    def load_meta_record(self, article_record):
        article_record["tags"], article_record["authors"] = self.retrieve_tags_authors(article_record["article_id"])

    def retrieve_tags_authors(self, article_id):
        tags, authors = [], []
        con = self.get_connection()
        for tag_row in con.query(self.tags_query, id=article_id):
            tags.append({"url": tag_row["TAG_URL"], "name": tag_row["TAG_NAME"]})
        for author_row in con.query(self.authors_query, id=article_id):
            authors.append({"url": author_row["AUT_URL"], "name": author_row["AUT_NAME"]})

        return tags, authors

    def load_articles(self, load_text=False, load_meta=False, limit = None):
        econ=self.engine.connect()

        article_info_sql= "SELECT AIN_ID, AIN_URL , AIN_TITLE, AIN_DATE FROM ARTICLE_INFO ORDER BY AIN_ID"
        if (limit):
            article_info_sql += ' LIMIT '+str(limit)
        articleDF = pd.read_sql(article_info_sql,  econ)
        articleDF.columns = ['article_id' , 'url', 'title', 'date_p' ]
        articleDF = self.load_text(articleDF, all=True,load_text=load_text)
 #      articleDF.reset_index(inplace=True, drop=True)
        econ.close()
        return articleDF


    def load_articles_with_text(self, id1, id2):
        article_info_sql= "SELECT AIN_ID, AIN_URL, AIN_TITLE, AIN_DATE, ATX_TEXT FROM ARTICLE_INFO, ARTICLE_TEXT WHERE ATX_AIN_ID = AIN_ID AND AIN_ID = :id"
        article_score_sql = "SELECT SCORE FROM TFIDF_SCORE_NORM T WHERE T.ID = :id AND T.OTHER_ID = :id2"
        con = self.get_connection()
        article1 = con.query(article_info_sql, {"id" : id1}).next()
        article2 = con.query(article_info_sql, {"id" : id2}).next()
        scorequery = con.query(article_score_sql, {"id" : id1, "id2" : id2})
        scoreres = scorequery.next()
        score = scoreres["SCORE"]
        article1["ATX_TEXT"] = self.sentence_tokenizer.clean_sentences(article1["ATX_TEXT"] )
        article2["ATX_TEXT"] = self.sentence_tokenizer.clean_sentences(article2["ATX_TEXT"] )

        return article1, article2, score


