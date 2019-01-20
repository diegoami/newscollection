import numpy as np
import logging


from sklearn.model_selection import cross_val_score, GridSearchCV, cross_val_predict
from sklearn.linear_model import SGDClassifier, SGDRegressor
from .common import retrieve_X_y_clf, retrieve_X_y_regr
from .scoring import print_best_parameters

sgd_clfr_params = {

'alpha': [1e-4, 1e-3, 1e-2, 1e-1], # learning rate
        'n_iter': [1000], # number of epochs
    'loss': ['log'], # logistic regression,
    'penalty': ['l2'],
'n_jobs': [-1]
    }

sgd_regr_params = {

'alpha': [1e-4, 1e-3, 1e-2, 1e-1], # learning rate



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


    clf =  GridSearchCV(SGDClassifier(), sgd_clfr_params, cv=5, scoring='f1')
    clf.fit(X_train, y_train, sample_weight=w1)
    print_best_parameters(clf)
    return clf.best_estimator_


def create_regressor(train_df):
    logging.info(" ============= REGRESSOR ====================== ")
    logging.info("train_df has {} rows".format(len(train_df)))

    X_train, y_train = retrieve_X_y_regr(train_df)

    clf =  GridSearchCV(SGDRegressor(), sgd_regr_params, cv=5, scoring='neg_mean_squared_error')

    logging.info("Regressor params")
    print_best_parameters(clf)

    clf.fit(X_train, y_train)
    print_best_parameters(clf)
    return clf.best_estimator_







