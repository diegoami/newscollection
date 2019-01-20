import logging
import numpy as np
from sklearn.externals import joblib
from .common import RELEVANT_COLUMNS

def predict(test_df,  xboost_model_file, xboost_classif_file, predictions_df, threshold=0.65):
    logging.info("removing already predicted....")

    merged_DF = test_df[~test_df.index.isin(predictions_df.index)]
    logging.info("merged_df has {} rows".format(len(merged_DF )))


    result_columns = 'SCO_USER'
    X_test = np.array(merged_DF[RELEVANT_COLUMNS])
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

    y_pred = clf.predict(X_test)
    merged_DF['SCO_PRED'] = y_pred

    merged_DF.reset_index(drop=False, inplace=True)
    return merged_DF
