from .article_repo import ArticleRepo
from datetime import datetime
import dataset
import sys, traceback
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from technews_nlp_aggregator.common.util import extract_source
similarArticlesSQL = \
"""
SELECT T.ID_1, T.ID_2, T.DATE_1, T.TITLE_1, T.TITLE_2, T.URL_1, T.URL_2, T.SIMILARITY AS T_SCORE, D.SIMILARITY AS D_SCORE FROM TFIDF_SCORE T
LEFT JOIN DOC2VEC_SCORE D ON D.ID_1=T.ID_1 AND D.ID_2=T.ID_2
ORDER BY T.DATE_1 DESC, T.SIMILARITY DESC
"""

class SimilarArticlesRepo:

    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.db = dataset.connect(self.db_connection ,  engine_kwargs = {
            'connect_args' : {'charset' : 'utf8'}
        })

        self.same_story_tbl = self.db['SAME_STORY']
        self.same_story_jobs_tbl = self.db['SAME_STORY_JOBS']

    def association_exists(self, first_id, second_id, agent):
        found_row = self.same_story_tbl.find_one(SST_AIN_ID_1=first_id, SST_AIN_ID_2=second_id, SST_AGENT=agent)
        return found_row

    def persist_job(self, start, end, agentname, thresholds):
        try:
            self.db.begin()

            row = self.same_story_jobs_tbl.insert(
                dict({
                    "SSJ_START": start,
                    "SSJ_END": end,
                    "SSJ_AGENT": agentname,
                    "SSJ_THRESHOLD_LO": thresholds[0],
                    "SSJ_THRESHOLD_HI": thresholds[1],

                    "SSJ_EXEC_DATE" : datetime.now()
                })
            )
            self.db.commit()
        except:
            traceback.print_exc()
            self.db.rollback()

    def persist_association(self, first_id, second_id, agent, similarity):
        if (first_id > second_id):
            first_id, second_id = second_id, first_id
        rowFound = self.association_exists(first_id, second_id, agent)

        if (not rowFound ):

            try:
                self.db.begin()

                row = self.same_story_tbl.insert(
                            dict({
                                "SST_AIN_ID_1" : first_id,
                                "SST_AIN_ID_2" : second_id,
                                "SST_AGENT" : agent,
                                "SST_SIMILARITY": similarity,
                                "SST_UPDATED"   : datetime.now()
                            })
                )
                self.db.commit()
            except:
                traceback.print_exc()
                self.db.rollback()
        else:
            pk = rowFound['SST_ID']
            try:
                self.db.begin()
                row = self.same_story_tbl.update(
                    dict({
                        "SST_ID" : pk,
                        "SST_AIN_ID_1": first_id,
                        "SST_AIN_ID_2": second_id,
                        "SST_AGENT": agent,
                        "SST_SIMILARITY": similarity,
                        "SST_UPDATED":  datetime.now()
                    }), ['SST_ID']
                )
                self.db.commit()
            except:
                traceback.print_exc()
                self.db.rollback()

    def list_similar_articles(self):
        similar_stories = []
        for row in self.db.query(similarArticlesSQL):
            similar_story = dict({
                "DATE_1"  : row["DATE_1"],
                "TITLE_1" : row["TITLE_1"],
                "TITLE_2" : row["TITLE_2"],
                "URL_1"   : row["URL_1"],
                "SOURCE_1" : extract_source(row["URL_1"]),
                "URL_2"   : row["URL_2"],
                "SOURCE_2": extract_source(row["URL_2"]),
                "T_SCORE" : row["T_SCORE"],
                "D_SCORE" : row["D_SCORE"]

            })
            similar_stories.append(similar_story)

        return similar_stories
