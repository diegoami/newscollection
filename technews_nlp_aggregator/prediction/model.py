import numpy as np
import logging
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score, GridSearchCV
from xgboost import XGBRegressor, XGBClassifier


def print_best_parameters( classifier):
    if hasattr(classifier, "best_estimator_"):
        best_parameters = classifier.best_estimator_.get_params()
        for param_name in sorted(best_parameters.keys()):
            logging.info("\t%s: %r" % (param_name, best_parameters[param_name]))



def create_classifier(train_df, xboost_classifier_file):

    model_returned = {}
    logging.info(" ============= CLASSIFIER ===================== ")
    logging.info("train_df has {} rows".format(len(train_df)))
    relevant_columns = ['SCO_DAYS', 'SCO_W_DAYS', 'SCO_D_TEXT', 'SCO_T_TEXT','SCO_D_TITLE',  'SCO_T_TITLE', 'SCO_T_SUMMARY', 'SCO_D_SUMMARY', 'SCO_T_SUMMARY_2', 'SCO_D_SUMMARY_2', 'SCO_CW_TITLE',  'SCO_CW_TEXT', 'SCO_CW_SUMMARY', 'SCO_CW_SUMMARY_2' ]

    result_columns = 'SCO_USER'
    X_train = np.array(train_df[relevant_columns])
    y_train = np.array(train_df[result_columns].map(lambda x: 1 if x > 0.8 else 0))

    logging.info("X_train: shape {}, y_train: shape {}".format(X_train.shape, y_train.shape))

    weight = float(len(y_train[y_train == 0]))/float(len(y_train[y_train == 1]))
    #w1 = np.ndarray(shape=(len(y_train)), dtype=float, order='F')
    logging.info("Weights: {}, {}".format(weight, 1-weight))

    w1 = np.array([1.0] * y_train.shape[0])
    w1[y_train==1] = 1.0-weight
    w1[y_train==0] = weight


    logging.info("Weights: {}, {}".format(w1.mean(), w1.sum()))



    model_returned["TMO_YCLF_MEAN"] = y_train.mean()
    xgb_clfr_params = {
        'learning_rate':[0.1],
        'max_depth' : [5],
        'min_child_weight' : [8],
        'colsample_bytree' : [0.7],
        'reg_alpha' : [0.1],
        'subsample': [0.9]
    }
    clf =  GridSearchCV(XGBClassifier(), xgb_clfr_params, cv=5, scoring='f1')

    logging.info("Classifier params")
    clf.fit(X_train, y_train,  sample_weight=w1)
    print_best_parameters(clf)

    f1 = cross_val_score(clf.best_estimator_, X_train, y_train, cv=5, scoring='f1')
    model_returned["TMO_F1"] = f1.mean()
    precision = cross_val_score(clf.best_estimator_, X_train, y_train, cv=5, scoring='precision')
    model_returned["TMO_PRECISION"] = precision.mean()
    recall = cross_val_score(clf.best_estimator_, X_train, y_train, cv=5, scoring='recall')
    model_returned["TMO_RECALL"] = recall.mean()

    accuracy = cross_val_score(clf.best_estimator_, X_train, y_train, cv=5, scoring='accuracy')
    model_returned["TMO_ACCURACY"] = accuracy.mean()
    neg_log_loss = cross_val_score(clf.best_estimator_, X_train, y_train, cv=5, scoring='neg_log_loss')
    model_returned["TMO_LOG_LOSS"] = neg_log_loss.mean()

    logging.info("Training set : {} data points".format(len(X_train)))
    logging.info("F1: %0.8f (+/- %0.8f)" % (f1.mean(), f1.std() * 2))
    logging.info("Precision: %0.8f (+/- %0.8f)" % (precision.mean(), precision.std() * 2))
    logging.info("Recall: %0.8f (+/- %0.8f)" % (recall.mean(), recall.std() * 2))
    logging.info("Accuracy: %0.8f (+/- %0.8f)" % (accuracy.mean(), accuracy.std() * 2))
    logging.info("Neg Log Loss: %0.8f (+/- %0.8f)" % (neg_log_loss.mean(), neg_log_loss.std() * 2))

    y_pred = clf.best_estimator_.predict(X_train)
    train_df['SCO_PRED'] = y_pred
    joblib.dump(clf.best_estimator_, xboost_classifier_file )
    clf_feature_report = {column: feature_imp for column, feature_imp in zip(relevant_columns, clf.best_estimator_.feature_importances_)}
    logging.info("Feature importances: {}".format(clf_feature_report ))
    return model_returned, clf_feature_report, clf.best_estimator_.get_params()


def create_regressor(train_df, xboost_model_file):
    model_returned = {}
    logging.info(" ============= REGRESSOR ====================== ")
    logging.info("train_df has {} rows".format(len(train_df)))

    # train_df = pd.read_csv(train_file, index_col=0)
    relevant_columns = ['SCO_DAYS', 'SCO_W_DAYS', 'SCO_D_TEXT', 'SCO_T_TEXT','SCO_D_TITLE',  'SCO_T_TITLE', 'SCO_T_SUMMARY', 'SCO_D_SUMMARY', 'SCO_T_SUMMARY_2', 'SCO_D_SUMMARY_2', 'SCO_CW_TITLE',  'SCO_CW_TEXT', 'SCO_CW_SUMMARY', 'SCO_CW_SUMMARY_2' ]

    result_columns = 'SCO_USER'
    X_train = np.array(train_df[relevant_columns])
    y_train = np.array(train_df[result_columns])
    logging.info("X_train: shape {}, y_train: shape {}".format(X_train.shape, y_train.shape))
    model_returned["TMO_YREG_MEAN"] = y_train.mean()

    xgb_regr_params = {
        'learning_rate':[ 0.1],
        'max_depth' : [5],
        'min_child_weight' : [5, 6],
        'colsample_bytree' : [0.6],
        'subsample' : [0.8],
        'reg_alpha' : [1]

    }
    clf =  GridSearchCV(XGBRegressor(), xgb_regr_params, cv=5, scoring='neg_mean_squared_error')

    logging.info("Regressor params")
    print_best_parameters(clf)

    clf.fit(X_train, y_train)
    print_best_parameters(clf)
    logging.info("Training set : {} data points".format(len(X_train)))
    neg_mean_squared_error = cross_val_score(clf.best_estimator_, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    model_returned["TMO_NMSE"] = neg_mean_squared_error.mean()
    logging.info("Neg Mean Squared Error: %0.8f (+/- %0.8f)" % (neg_mean_squared_error.mean(), neg_mean_squared_error .std() * 2))

    joblib.dump(clf.best_estimator_, xboost_model_file)
    regr_feature_report = {column: feature_imp for column, feature_imp in zip(relevant_columns, clf.best_estimator_.feature_importances_)}
    return model_returned, regr_feature_report, clf.best_estimator_.get_params()



def predict(test_df,  xboost_model_file, xboost_classif_file, predictions_df):
    logging.info("setting index....")

    test_df.set_index(['SCO_AIN_ID_1', 'SCO_AIN_ID_2'], inplace=True)
    logging.info("removing already predicted....")

    merged_DF = test_df[~test_df.index.isin(predictions_df.index)]
    logging.info("merged_df has {} rows".format(len(merged_DF )))

    relevant_columns = ['SCO_DAYS', 'SCO_W_DAYS', 'SCO_D_TEXT', 'SCO_T_TEXT','SCO_D_TITLE',  'SCO_T_TITLE', 'SCO_T_SUMMARY', 'SCO_D_SUMMARY', 'SCO_T_SUMMARY_2', 'SCO_D_SUMMARY_2', 'SCO_CW_TITLE',  'SCO_CW_TEXT', 'SCO_CW_SUMMARY', 'SCO_CW_SUMMARY_2' ]
    result_columns = 'SCO_USER'
    X_test = np.array(merged_DF[relevant_columns])
    clf = joblib.load(xboost_model_file)
    logging.info("Regressor params")
    logging.info(clf.get_params())

    y_test = clf.predict(X_test)
    merged_DF['SCO_REGR'] = y_test

    clf_clas = joblib.load(xboost_classif_file)
    logging.info("Classifier params")
    logging.info(clf_clas.get_params())

    y_clas = clf_clas.predict_proba(X_test)
    merged_DF['SCO_PROBA']  = y_clas[:,1]

    merged_DF.reset_index(drop=False, inplace=True)
    return merged_DF
