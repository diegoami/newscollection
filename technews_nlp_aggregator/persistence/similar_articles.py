from .article_repo import ArticleRepo
from datetime import datetime
import dataset
import sys, traceback
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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
