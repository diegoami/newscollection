

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


def print_best_parameters( classifier):
    if hasattr(classifier, "best_estimator_"):
        best_parameters = classifier.best_estimator_.get_params()
        for param_name in sorted(best_parameters.keys()):
            print("\t%s: %r" % (param_name, best_parameters[param_name]))


def create_classifier(train_DF, train_file_aug, xboost_model_file):
  # train_df = pd.read_csv(train_file, index_col=0)
    relevant_columns = ['SCO_DAYS','SCO_D_TEXT', 'SCO_T_TEXT','SCO_D_TITLE',  'SCO_T_TITLE', 'SCO_T_SUMMARY', 'SCO_D_SUMMARY', 'SCO_T_SUMMARY_2', 'SCO_D_SUMMARY_2', 'SCO_CW_TITLE',  'SCO_CW_TEXT', 'SCO_CW_SUMMARY', 'SCO_CW_SUMMARY_2' ]

    result_columns = 'SCO_USER'
    X_train = np.array(train_df[relevant_columns])
    y_train = np.array(train_df[result_columns])
    xgbparams = {
        #'learning_rate':[ 0.001, 0.005, 0.01, 0.05, 0.1],
        #'n_estimators' : [100,200,500]
        #'max_depth' : [2,3,4], 'min_child_weight' : [5,6,7]
        #'colsample_bytree' : [0.6, 0.7, 0.8]
        #'reg_alpha' : [0, 0.1, 0.001, 0.0001]
        #'learning_rate' : [0.1, 0.01], 'n_estimators' : [100,200]

    }
    #clf =  GridSearchCV(XGBRegressor(max_depth=3, min_child_weight=6, gamma=0,colsample_bytree=0.8,subsample=0.8, reg_alpha=0.01, learning_rate=0.1), xgbparams)
    #clf =  GridSearchCV(XGBRegressor(max_depth=3, min_child_weight=6, subsample=0.7,colsample_bytree=0.6,reg_alpha=0.001), xgbparams)


    clf = XGBRegressor(max_depth=3, min_child_weight=6, subsample=0.7,colsample_bytree=0.6,reg_alpha=0.001)
    clf.fit(X_train, y_train)
   # clf = XGBRegressor(min_child_weight=1,max_depth=3).fit(X_train,y_train)
    scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    #print_best_parameters(clf)
    print("Training set : {} data points".format(len(X_train)))
    print(scores)
    print("Error: %0.8f (+/- %0.8f)" % (scores.mean(), scores.std() * 2))
    y_pred = clf.predict(X_train)

    train_df['SCO_PRED'] = y_pred
    train_df.to_csv(train_file_aug)
  #  print(clf.best_estimator_)

  #  print(clf.best_estimator_.feature_importances_)


    joblib.dump(clf, xboost_model_file)


if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))
    db_config = yaml.safe_load(open(config["key_file"]))
    db_url = db_config["db_url"]
    similarArticlesRepo = ArticlesSimilarRepo(db_url)

    train_file = config["train_data_file"]

    #train_df = pd.read_csv(train_file, index_col=0)
    train_df = similarArticlesRepo.load_train_set()
    train_file_aug = config["train_data_file_aug"]
    xboost_model_file = config["xgboost_model_file"]

    create_classifier(train_df, train_file_aug, xboost_model_file)