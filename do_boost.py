

import xgboost as xgb

from xgboost import XGBRegressor, XGBClassifier
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
import pandas as pd
import numpy as np
import yaml
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV


def print_best_parameters( classifier):
    if hasattr(classifier, "best_estimator_"):
        best_parameters = classifier.best_estimator_.get_params()
        for param_name in sorted(best_parameters.keys()):
            print("\t%s: %r" % (param_name, best_parameters[param_name]))


def create_classifier(config):
    train_df = pd.read_csv('data/scores_p.csv', index_col=0)
   # relevant_columns = ['SCO_DAYS', 'SCO_D_SUMMARY', 'SCO_D_TEXT', 'SCO_D_TITLE', 'SCO_T_SUMMARY', 'SCO_T_TEXT',
     #                   'SCO_T_TITLE']
  #  relevant_columns = ['SCO_DAYS', 'SCO_D_TEXT', 'SCO_T_TEXT','SCO_D_TITLE',  'SCO_T_TEXT' ]
    #relevant_columns = ['SCO_DAYS', 'SCO_D_TEXT', 'SCO_T_TEXT','SCO_D_TITLE',  'SCO_T_TITLE' ]
    relevant_columns = ['SCO_DAYS','SCO_D_TEXT', 'SCO_T_TEXT','SCO_D_TITLE',  'SCO_T_TITLE', 'SCO_T_SUMMARY', 'SCO_D_SUMMARY' ]
    result_columns = 'SCO_USER'
    X_train = np.array(train_df[relevant_columns])
    y_train = np.array(train_df[result_columns])
    xgbparams = {
        'learning_rate':[ 0.001, 0.005, 0.01, 0.05, 0.1],
        'n_estimators' : [100,200,500]
    }
    clf =  GridSearchCV(XGBRegressor(max_depth=3, min_child_weight=6, gamma=0,colsample_bytree=0.8,subsample=0.8, reg_alpha=0.01, learning_rate=0.1), xgbparams)
    clf.fit(X_train, y_train)
   # clf = XGBRegressor(min_child_weight=1,max_depth=3).fit(X_train,y_train)
    scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    print_best_parameters(clf)
    print(scores)
    print("Error: %0.8f (+/- %0.8f)" % (scores.mean(), scores.std() * 2))
    y_pred = clf.predict(X_train)
    print(y_pred)
    train_df['SCO_PRED'] = y_pred
    train_df.to_csv('data/scores_p_pr.csv')
    print(clf.best_estimator_)
    print(clf.best_estimator_)
    print(clf.best_estimator_.feature_importances_)


    #joblib.dump(clf, config["pickle_dir"] + 'xgbregressor.pkl')


if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))
    create_classifier(config)