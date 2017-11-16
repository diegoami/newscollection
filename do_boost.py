

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
    relevant_columns = ['SCO_DAYS', 'SCO_D_SUMMARY', 'SCO_D_TEXT', 'SCO_D_TITLE', 'SCO_T_SUMMARY', 'SCO_T_TEXT',
                        'SCO_T_TITLE']
    result_columns = 'SCO_USER'
    X_train = np.array(train_df[relevant_columns])
    y_train = np.array(train_df[result_columns])
    xgbparams = {
        "max_depth" : [3,5,7,9], "min_child_weight" : [2,3,5,8,10]
    }
    clf =  GridSearchCV(XGBRegressor(), xgbparams)
    clf.fit(X_train, y_train)
    scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    print_best_parameters(clf)
    print(scores)
    print("Error: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    y_pred = clf.predict(X_train)
    print(y_pred)
    train_df['SCO_PRED'] = y_pred
    train_df.to_csv('data/scores_p_pr.csv')
    print(clf.__dict__)
    joblib.dump(clf, config["pickle_dir"] + 'xgbregressor.pkl')


if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))
    create_classifier(config)