import logging
import traceback
from datetime import datetime

import dataset
from technews_nlp_aggregator.nlp_model.common import defaultTokenizer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import re
from technews_nlp_aggregator.common.util import extract_source

similarArticlesSQL_select = \
"""
SELECT T.ID_1, T.ID_2, T.DATE_1, T.TITLE_1, T.TITLE_2, T.URL_1, T.URL_2, ROUND(T.SIMILARITY,3) AS T_SCORE
  , ROUND(D.SIMILARITY,3) AS D_SCORE, ROUND(U.SSU_SIMILARITY_AVG,3) AS U_SCORE FROM TFIDF_SCORE T
LEFT JOIN DOC2VEC_SCORE D ON D.ID_1=T.ID_1 AND D.ID_2=T.ID_2
LEFT JOIN (SELECT AVG(SSU_SIMILARITY) SSU_SIMILARITY_AVG, SSU_AIN_ID_1, SSU_AIN_ID_2 FROM SAME_STORY_USER GROUP BY SSU_AIN_ID_1, SSU_AIN_ID_2) U
ON T.ID_1=U.SSU_AIN_ID_1 AND T.ID_2=U.SSU_AIN_ID_2
"""

similarArticlesSQL_orderby = \
"""
 ORDER BY T.DATE_1 DESC, T.ID_1 DESC, T.SIMILARITY DESC
"""



controversialArticlesSQL = \
"""
SELECT ID, DATE, TITLE, URL, SUM_SCORE FROM CONTROVERSIAL_ARTICLES C WHERE DATE BETWEEN :start AND :end
"""

relatedArticlesSQL = \
"""
SELECT OTHER_ID AS O_ID, OTHER_DATE AS DATE, OTHER_TITLE AS TITLE, OTHER_URL AS URL, SCORE FROM TFIDF_SCORE_NORM WHERE ID = :id
"""


FLOAT_REGEX = re.compile('\d+(\.\d+)?')
class SimilarArticlesRepo:

    def get_connection(self):
        con = dataset.connect(self.db_connection, engine_kwargs={
            'connect_args': {'charset': 'utf8'}
        })
        return con



    def __init__(self, db_connection):
        self.db_connection = db_connection

       # self.same_story_tbl = self.db['SAME_STORY']
      #  self.same_story_jobs_tbl = self.db['SAME_STORY_JOBS']
      #  self.same_story_user_tbl = self.db['SAME_STORY_USER']



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

            allowed_tokens = ["T_SCORE", "D_SCORE", "U_SCORE", "OR", "AND", "(", ")", "NOT", "=", "<", ">", "<=", ">=", "<>", "IS", "NULL"]
            sp_tokens = defaultTokenizer.word_tokenizer.tokenize_fulldoc(filter_criteria)
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

    def similar_having_condition(self, filter_criteria=None):
        columnMap = {"tfidf" : "T_SCORE", "doc2vec" : "D_SCORE", "uscore" : "U_SCORE"}
        conditions = []
        condition_string = ""
        if filter_criteria:
            filter_parts = filter_criteria.split(',')
            for filter_part in filter_parts:
                filter_part_l = filter_part.split()
                if (len(filter_part_l) == 3):
                    column, operator, value = filter_part_l
                    column = column.lower()
                    if column in columnMap:
                        conditions.append(columnMap[column] + " "+operator+" "+ value)
                    else:
                        logging.info("Could not find column : {}".format(column))

                else:
                    logging.info("Not enough operators : {}".format(filter_part) )
            if len(conditions) > 0:
                condition_string = condition_string + " HAVING "
            for index, condition in enumerate(conditions):
                if index > 0:
                    condition_string = condition_string + " AND "

                condition_string = condition_string + condition
        return condition_string

    def list_similar_articles(self, filter_criteria= None):
        similar_stories = []
        con = self.get_connection()
        similarArticlesSQL_having_cond =  "HAVING "+filter_criteria if self.verify_having_condition(filter_criteria) else ""
        similarArticlesSQL = similarArticlesSQL_select + similarArticlesSQL_having_cond + similarArticlesSQL_orderby
        for row in con.query(similarArticlesSQL):
            similar_story = dict({
                "ID_1": row["ID_1"],
                "ID_2": row["ID_2"],
                "DATE_1"  : row["DATE_1"],
                "TITLE_1" : row["TITLE_1"],
                "TITLE_2" : row["TITLE_2"],
                "URL_1"   : row["URL_1"],
                "SOURCE_1" : extract_source(row["URL_1"]),
                "URL_2"   : row["URL_2"],
                "SOURCE_2": extract_source(row["URL_2"]),
                "T_SCORE" : row["T_SCORE"],
                "D_SCORE" : row["D_SCORE"],
                "U_SCORE": row["U_SCORE"]

            })
            if (similar_story["U_SCORE"] is not None):
                similar_story["U_SCORE_DEF"] = True
            if (similar_story["SOURCE_1"] != similar_story["SOURCE_2"]):
                similar_stories.append(similar_story)

        return similar_stories

