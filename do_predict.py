

import xgboost as xgb

from xgboost import XGBRegressor, XGBClassifier
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
import pandas as pd
import numpy as np
import yaml
from technews_nlp_aggregator.persistence.articles_similar_repo import  ArticlesSimilarRepo
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV




def predict(test_DF, test_file_aug, xboost_model_file):
  # train_df = pd.read_csv(train_file, index_col=0)

    relevant_columns = ['SCO_DAYS','SCO_D_TEXT', 'SCO_T_TEXT','SCO_D_TITLE',  'SCO_T_TITLE', 'SCO_T_SUMMARY', 'SCO_D_SUMMARY', 'SCO_T_SUMMARY_2', 'SCO_D_SUMMARY_2', 'SCO_CW_TITLE',  'SCO_CW_TEXT', 'SCO_CW_SUMMARY', 'SCO_CW_SUMMARY_2' ]
    result_columns = 'SCO_USER'
    X_test = np.array(test_df[relevant_columns])
    clf = joblib.load(xboost_model_file)
    y_test = clf.predict(X_test)
    test_df['SCO_PRED'] = y_test
    test_df.to_csv(test_file_aug)
    return test_df

if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))
    db_config = yaml.safe_load(open(config["key_file"]))
    db_url = db_config["db_url"]
    similarArticlesRepo = ArticlesSimilarRepo(db_url)



    #train_df = pd.read_csv(train_file, index_col=0)
    test_df = similarArticlesRepo.load_test_set()
    test_file_aug = config["test_data_file_aug"]
    version = config["version"]

    xboost_model_file = config["xgboost_model_file"]

    test_df_res = predict(test_df, test_file_aug, xboost_model_file)
    similarArticlesRepo.write_predictions(test_df_res, version)