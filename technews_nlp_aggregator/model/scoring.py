import logging
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, log_loss

from sklearn.metrics import roc_auc_score
from .common import RELEVANT_COLUMNS, retrieve_X_y_clf

def print_best_parameters( classifier):
    if hasattr(classifier, "best_estimator_"):
        best_parameters = classifier.best_estimator_.get_params()
        for param_name in sorted(best_parameters.keys()):
            logging.info("\t%s: %r" % (param_name, best_parameters[param_name]))


def threshold_scores_clf(clf, train_df, method="predict_proba", threshold=0.65):
    X_train, y_train = retrieve_X_y_clf(train_df)
    scores = {}
    y_scores = cross_val_predict(clf, X_train, y_train, cv=5, method=method)
    threshold_range = [0.6 + x * 0.01 for x in range(0, 35)]

    f1 = f1_score(y_train, y_scores[:, 1] > threshold)
    scores["TMO_F1"] = f1
    precision = precision_score(y_train, y_scores[:, 1] > threshold)
    scores["TMO_PRECISION"] = precision
    recall = recall_score(y_train, y_scores[:, 1] > threshold)
    scores["TMO_RECALL"] = recall
    accuracy = accuracy_score(y_train, y_scores[:, 1] > threshold)
    scores["TMO_ACCURACY"] = accuracy
    log_loss = accuracy_score(y_train, y_scores[:, 1] > threshold)
    scores["TMO_LOG_LOSS"] = log_loss
    roc_auc = roc_auc_score(y_train, y_scores[:, 1] > threshold)
    scores["TMO_ROC_AUC"] = roc_auc

    return scores

def cross_val_score_clf(clf, train_df):
    X_train, y_train = retrieve_X_y_clf(train_df)
    scores = {}
    f1 = cross_val_score(clf, X_train, y_train , cv=5, scoring='f1')
    scores["TMO_F1"] = f1.mean()
    precision = cross_val_score(clf, X_train, y_train, cv=5, scoring='precision')
    scores["TMO_PRECISION"] = precision.mean()
    recall = cross_val_score(clf, X_train, y_train, cv=5, scoring='recall')
    scores["TMO_RECALL"] = recall.mean()

    accuracy = cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy')
    scores["TMO_ACCURACY"] = accuracy.mean()
    neg_log_loss = cross_val_score(clf, X_train, y_train, cv=5, scoring='neg_log_loss')
    scores["TMO_LOG_LOSS"] = neg_log_loss.mean()

    logging.info("Training set : {} data points".format(len(X_train)))
    logging.info("F1: %0.8f (+/- %0.8f)" % (f1.mean(), f1.std() * 2))
    logging.info("Precision: %0.8f (+/- %0.8f)" % (precision.mean(), precision.std() * 2))
    logging.info("Recall: %0.8f (+/- %0.8f)" % (recall.mean(), recall.std() * 2))
    logging.info("Accuracy: %0.8f (+/- %0.8f)" % (accuracy.mean(), accuracy.std() * 2))
    logging.info("Neg Log Loss: %0.8f (+/- %0.8f)" % (neg_log_loss.mean(), neg_log_loss.std() * 2))

    return scores


def cross_val_score_regr(clf, train_df):
    X_train, y_train = retrieve_X_y_clf(train_df)
    scores = {}
    neg_mean_squared_error = cross_val_score(clf, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    scores["TMO_NMSE"] = neg_mean_squared_error.mean()
    logging.info(
        "Neg Mean Squared Error: %0.8f (+/- %0.8f)" % (neg_mean_squared_error.mean(), neg_mean_squared_error.std() * 2))

    return scores

def feature_importances(clf):
    feature_report = {column: feature_imp for column, feature_imp in
                           zip(RELEVANT_COLUMNS, clf.feature_importances_)}

    logging.info("Feature importances: {}".format(feature_report ))
    return feature_report