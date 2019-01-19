import numpy as np
import logging


from sklearn.model_selection import cross_val_score, GridSearchCV, cross_val_predict
from xgboost import XGBRegressor, XGBClassifier
from .common import retrieve_X_y_clf, retrieve_X_y_regr
from .scoring import print_best_parameters

xgb_clfr_params = {
        'learning_rate':[0.1],
        'max_depth' : [5],
        'min_child_weight' : [8],
        'colsample_bytree' : [0.7],
        'reg_alpha' : [0.1],
        'subsample': [0.9]
    }

xgb_regr_params = {
    'learning_rate': [0.1],
    'max_depth': [5],
    'min_child_weight': [5, 6],
    'colsample_bytree': [0.6],
    'subsample': [0.8],
    'reg_alpha': [1]

}

def create_classifier(train_df):

    logging.info(" ============= CLASSIFIER ===================== ")
    logging.info("train_df has {} rows".format(len(train_df)))

    X_train, y_train = retrieve_X_y_clf(train_df)

    logging.info("X_train: shape {}, y_train: shape {}".format(X_train.shape, y_train.shape))

    weight = float(len(y_train[y_train == 0]))/float(len(y_train[y_train == 1]))

    logging.info("Weights: 0 : {}, 1: {}".format(weight, 1-weight))

    w1 = np.array([1.0] * y_train.shape[0])
    w1[y_train==1] = 1.0-weight
    w1[y_train==0] = weight


    clf =  GridSearchCV(XGBClassifier(), xgb_clfr_params, cv=5, scoring='f1')
    clf.fit(X_train, y_train, sample_weight=w1)
    print_best_parameters(clf)
    return clf


def create_regressor(train_df):
    logging.info(" ============= REGRESSOR ====================== ")
    logging.info("train_df has {} rows".format(len(train_df)))

    X_train, y_train = retrieve_X_y_regr(train_df)

    clf =  GridSearchCV(XGBRegressor(), xgb_regr_params, cv=5, scoring='neg_mean_squared_error')

    logging.info("Regressor params")
    print_best_parameters(clf)

    clf.fit(X_train, y_train)
    print_best_parameters(clf)
    return clf







