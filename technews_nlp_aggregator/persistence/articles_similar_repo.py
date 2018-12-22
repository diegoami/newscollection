import logging
import traceback
from datetime import datetime
import pandas as pd
import dataset
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer

from sqlalchemy import create_engine

import re
from technews_nlp_aggregator.common.util import extract_source_without_www

similarArticlesSQL_select = \
"""
SELECT * FROM P_SCORES 
  WHERE P_SCORE > 0.01 
"""

similarArticlesSQL_orderby = \
"""
  ORDER BY DATE_2 DESC, DATE_1 DESC, U_SCORE DESC, P_SCORE DESC, TITLE_2 DESC, TITLE_1 DESC
"""


FLOAT_REGEX = re.compile('\d+(\.\d+)?')
class ArticlesSimilarRepo:

    def get_connection(self):
        return self.dataset_connection

    def     __init__(self, db_connection):
        self.db_connection = db_connection

        self.dataset_connection = dataset.connect(self.db_connection, engine_kwargs={
            'connect_args': {'charset': 'utf8'}
        })
        self.engine = self.dataset_connection.engine


    def association_exists(self, con, first_id, second_id, agent):

        found_row = con['SAME_STORY'].find_one(SST_AIN_ID_1=first_id, SST_AIN_ID_2=second_id, SST_AGENT=agent)
        return found_row

    def persist_job(self, start, end, agentname, thresholds):
        con = self.get_connection()
        try:

            con.begin()

            row = con['SAME_STORY_JOBS'].insert(
                dict({
                    "SSJ_START": start,
                    "SSJ_END": end,
                    "SSJ_AGENT": agentname,
                    "SSJ_THRESHOLD_LO": thresholds[0],
                    "SSJ_THRESHOLD_HI": thresholds[1],

                    "SSJ_EXEC_DATE" : datetime.now()
                })
            )
            con.commit()
        except:
            traceback.print_exc()
            con.rollback()

    def override_user_association(self, first_id, second_id, similarity, origin):
        if (first_id > second_id):
            first_id, second_id = second_id, first_id
        con = self.get_connection()

        try:
            con.begin()

            row = con['SAME_STORY_USER'].update(
                dict({
                    "SSU_AIN_ID_1": first_id,
                    "SSU_AIN_ID_2": second_id,
                    "SSU_ORIGIN": origin,
                    "SSU_SIMILARITY": similarity,
                    "SSU_UPDATED": datetime.now()
                })
            )
            con.commit()
        except:
            traceback.print_exc()
            con.rollback()

    def persist_user_association(self, first_id, second_id, similarity, origin):
        if (first_id > second_id):
            first_id, second_id = second_id, first_id
        con = self.get_connection()

        try:
            con.begin()

            row = con['SAME_STORY_USER'].insert(
                        dict({
                            "SSU_AIN_ID_1" : first_id,
                            "SSU_AIN_ID_2" : second_id,
                            "SSU_ORIGIN" : origin,
                            "SSU_SIMILARITY": similarity,
                            "SSU_UPDATED"   : datetime.now()
                        })
            )
            con.commit()
        except:
            traceback.print_exc()
            con.rollback()


    def persist_association(self, con, first_id, second_id, agent, similarity):
        if (first_id > second_id):
            first_id, second_id = second_id, first_id

        rowFound = self.association_exists(con, first_id, second_id, agent)

        if (not rowFound ):

            row = con['SAME_STORY'].insert(
                        dict({
                            "SST_AIN_ID_1" : first_id,
                            "SST_AIN_ID_2" : second_id,
                            "SST_AGENT" : agent,
                            "SST_SIMILARITY": similarity,
                            "SST_UPDATED"   : datetime.now()
                        })
            )

        else:
            pk = rowFound['SST_ID']
            row = con['SAME_STORY'].update(
                dict({
                    "SST_ID" : pk,
                    "SST_AIN_ID_1": first_id,
                    "SST_AIN_ID_2": second_id,
                    "SST_AGENT": agent,
                    "SST_SIMILARITY": similarity,
                    "SST_UPDATED":  datetime.now()
                }), ['SST_ID']
            )


    def verify_having_condition(self, filter_criteria=None):
        if filter_criteria:

            allowed_tokens = ["U_SCORE", "P_SCORE",  "OR", "AND", "(", ")", "NOT", "=", "<", ">", "<=", ">=", "<>", "IS", "NULL"]
            sp_tokens = defaultTokenizer.word_tokenizer.simple_tokenize(filter_criteria)
            if (len(sp_tokens ) >= 3):
                for sp_token in sp_tokens:
                    if (len(sp_token.strip()) == 0):
                        continue
                    token = sp_token.upper()
                    if not ( token in allowed_tokens or FLOAT_REGEX.match(token)):
                        logging.warning("INVALID TOKEN "+token)
                        raise ValueError("Condition containing invalid token")

                return True
        return False


    def retrieve_random_related(self):

        retrieveSQL = "select SST_AIN_ID_1 AS ID_1, SST_AIN_ID_2 AS ID_2 from SAME_STORY order by rand() limit 1"
        con = self.get_connection()
        row =  con.query(retrieveSQL).next()
        id1, id2   =  row["ID_1"], row["ID_2"]
        return id1, id2

    def list_similar_articles(self, version, filter_criteria= None):
        similar_stories = []

        econ = self.engine.connect()
        similarArticlesSQL_having_version = " AND VERSION = "+str(version)

        similarArticlesSQL_having_cond =  ( " AND ( " + filter_criteria +" ) " )  if self.verify_having_condition(filter_criteria) else ""
        similarArticlesSQL = similarArticlesSQL_select + similarArticlesSQL_having_version + similarArticlesSQL_having_cond + similarArticlesSQL_orderby+ " LIMIT 10000"
        similarArticlesDF = pd.read_sql(similarArticlesSQL , econ)
        similarArticlesDF["SOURCE_1"] = similarArticlesDF["URL_1"].map(extract_source_without_www)
        similarArticlesDF["SOURCE_2"] = similarArticlesDF["URL_2"].map(extract_source_without_www)
        similarArticlesDF["U_SCORE"].fillna(-1, inplace=True)
        econ.close()
        return similarArticlesDF

    def get_last_similar_story(self):
        sql_last_similar = "SELECT AIN_DATE FROM ARTICLE_INFO WHERE AIN_ID = (SELECT MAX(SST_AIN_ID_2) FROM SAME_STORY )"
        con = self.get_connection()
        max_date_query = con.query(sql_last_similar)
        max_date = next(max_date_query, None)
        return max_date["AIN_DATE"]

    def retrieve_user_paired(self):
        sql_user_similar = "SELECT SSU_AIN_ID_1, SSU_AIN_ID_2, AVG(SSU_SIMILARITY) AS SSU_SIMILARITY FROM SAME_STORY_USER GROUP BY SSU_AIN_ID_1, SSU_AIN_ID_2  ORDER BY  SSU_AIN_ID_1, SSU_AIN_ID_2"
        similar_stories = []
        con = self.get_connection()
        query_result= con.query(sql_user_similar)
        result = [row for row in query_result]
        return result

    def retrieve_ssus_for_id(self, id):
        sql_user_similar = "SELECT SSU_AIN_ID_1, SSU_AIN_ID_2, AVG(SSU_SIMILARITY) AS SSU_SIMILARITY FROM SAME_STORY_USER WHERE SSU_AIN_ID_1 = :id OR SSU_AIN_ID_2 = :id GROUP BY SSU_AIN_ID_1, SSU_AIN_ID_2  ORDER BY  SSU_AIN_ID_1, SSU_AIN_ID_2"
        similar_stories = []
        con = self.get_connection()
        query_result= con.query(sql_user_similar,  {"id": id})
        result = pd.DataFrame(columns=["article_id", "u_score"])
        for row in query_result:
            if (row["SSU_AIN_ID_1"] == id):
                result = result.append({"article_id": int(row["SSU_AIN_ID_2"]), "u_score": row["SSU_SIMILARITY"]}, ignore_index=True)
            elif (row["SSU_AIN_ID_2"] == id):
                result = result.append({"article_id": int(row["SSU_AIN_ID_1"]), "u_score": row["SSU_SIMILARITY"]}, ignore_index=True)


        return result

    def retrieve_sscs_for_id(self, id, version):
        sql_classif_similar = "SELECT PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_PROBA FROM PREDICTIONS WHERE ( PRED_AIN_ID_1=:id OR PRED_AIN_ID_2=:id ) AND PRED_VERSION = :version"
        similar_stories = []
        con = self.get_connection()
        query_result = con.query(sql_classif_similar , {"id": id, "version" : version})
        result = pd.DataFrame(columns=["article_id", "p_score"])
        for row in query_result:
            if (row["PRED_AIN_ID_1"] == id):
                result  = result.append({"article_id" : int(row["PRED_AIN_ID_2"]) , "p_score" : row["PRED_PROBA"]}, ignore_index=True)
            elif (row["PRED_AIN_ID_2"] == id):
                result = result.append({"article_id" : int(row["PRED_AIN_ID_1"]) , "p_score" : row["PRED_PROBA"]}, ignore_index=True)


        return result


    def retrieve_classif_paired(self, threshold, version):
        sql_classif_found = "SELECT PRED_AIN_ID_1, PRED_AIN_ID_2, 1 FROM PREDICTIONS WHERE NOT EXISTS (SELECT SSU_AIN_ID_1, SSU_AIN_ID_2 FROM SAME_STORY_USER WHERE PRED_AIN_ID_1 = SSU_AIN_ID_1 AND PRED_AIN_ID_2 = SSU_AIN_ID_2) AND PRED_PROBA >= :threshold AND PRED_VERSION = :version"
        similar_stories = []
        con = self.get_connection()
        query_result= con.query(sql_classif_found, {"threshold": threshold, "version" : version})
        result = [row for row in query_result]
        return result

    def update_to_processed(self, article_id, con=None):
        sql_update = "UPDATE ARTICLE_INFO SET AIN_PROCESSED = SYSDATE() WHERE AIN_ID = :article_id"
        con = self.get_connection() if not con else con
        article_query = con.query(sql_update, {"article_id": article_id})
        return

    def retrieve_similar_since(self, dateArg):

        sqlSimilarSince = "SELECT SST_AIN_ID_1, SST_AIN_ID_2 FROM SAME_STORY, ARTICLE_INFO WHERE SST_AIN_ID_1 = AIN_ID  AND  AIN_DATE >= ( :dateArg ) ORDER BY AIN_DATE DESC"
        con = self.get_connection()
        query_result = con.query(sqlSimilarSince, {"dateArg": dateArg})
        result = [row for row in query_result]
        return result



    def insert_score(self, score, con=None):
        con = con if con else self.get_connection()
        found_row = self.score_exists(score, con)
        if found_row:
            logging.info("Found row for score : {}".format(score))
        else:
            try:
                con.begin()
                logging.info("Trying to insert score : {}".format(score))
                row = con['SCORES'].insert(score)
                con.commit()
            except:
                traceback.print_exc()
                con.rollback()

    def update_score(self, score, con=None):
        con = con if con else self.get_connection()
        try:
            con.begin()
            logging.info("Trying to update score : {}".format(score))
            row = con['SCORES'].update(score,['SCO_ID'])
            con.commit()
        except:
            traceback.print_exc()
            con.rollback()


    def score_exists(self,  score, con):
        found_score = con['SCORES'].find_one(SCO_AIN_ID_1=score["SCO_AIN_ID_1"], SCO_AIN_ID_2=score["SCO_AIN_ID_2"],
                                           SCO_VERSION=score["SCO_VERSION"])
        return found_score

    def load_train_set(self, version):
        view_sql = "SELECT * FROM TRAIN_SCORES WHERE SCO_VERSION = "+str(version)
        econ = self.engine.connect()
        viewDF = pd.read_sql(view_sql, econ)
        econ.close()
        return viewDF

    def load_predictions(self, version):
        view_sql = "SELECT * FROM PREDICTIONS WHERE PRED_VERSION = "+str(version)
        econ = self.engine.connect()
        viewDF = pd.read_sql(view_sql, econ)
        viewDF.set_index(['PRED_AIN_ID_1', 'PRED_AIN_ID_2'], inplace=True)

        econ.close()
        return viewDF

    def load_test_set(self, version):
        view_sql =  "SELECT *  FROM TEST_SCORES WHERE SCO_VERSION = "+str(version)

        econ = self.engine.connect()
        viewDF = pd.read_sql(view_sql, econ)
        econ.close()
        return viewDF

    def write_predictions(self, test_df, version):
        con =  self.get_connection()

        replace_sql = 'INSERT into PREDICTIONS (PRED_AIN_ID_1, PRED_AIN_ID_2, PRED_REGR, PRED_PROBA, PRED_VERSION) values (:pred1,:pred2,:regr, :proba,:ver)'
        count = 0
#        exist_sql = 'SELECT FROM PREDICTION WHERE PRED_AIN_ID_1=:pred1 AND PRED_AIN_ID_2=:pred2 AND PRED_VERSION:ver, '
        con.begin()
        for index, row in test_df.iterrows():
            con.query(replace_sql, {'pred1' : row['SCO_AIN_ID_1'], 'pred2' : row['SCO_AIN_ID_2'], 'regr' : row['SCO_REGR'], 'proba' : row['SCO_PROBA'], 'ver' : version})
            if (count % 1000 == 0):
                logging.info("At {} predictions".format(count))
            count = count + 1
        con.commit()
