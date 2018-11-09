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


