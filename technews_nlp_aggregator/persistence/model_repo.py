from datetime import datetime
import dataset
import pandas as pd
import traceback
from sqlalchemy import create_engine

class ModelRepo:

    def get_connection(self):
        return self.dataset_connection

    def __init__(self, db_connection):
        self.db_connection = db_connection

        self.dataset_connection = dataset.connect(self.db_connection, engine_kwargs={
            'connect_args': {'charset': 'utf8'}
        })
        self.engine = self.dataset_connection.engine


    def save_model_performance(self, training_model):

        found = False
        con = self.get_connection()
        try:
            con.begin()
            pk = con['TRAINING_MODEL'].insert(
                   training_model
            )
            con.commit()
            print("Saved model")
        except:
            traceback.print_exc()
            con.rollback()

    def load_model_performances(self):
        found = False
        con = self.get_connection()

        return con['TRAINING_MODEL'].find(order_by=['-TMO_DATE'], _limit=20)

    def save_feature_report(self, report_type, report_str):
        found = False
        con = self.get_connection()
        try:
            con.begin()
            pk = con['FEATURE_REPORT'].insert(
                {'FRE_DATE' : datetime.now(),
                 'FRE_TYPE' : report_type,

                 'FRE_REPORT' : report_str})
            con.commit()
            print("Saved feature report")
        except:
            traceback.print_exc()
            con.rollback()

    def load_feature_reports(self):
        found = False
        con = self.get_connection()
        return con['FEATURE_REPORT'].find(order_by=['-FRE_DATE'], _limit=20)