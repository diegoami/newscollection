import numpy as np
import yaml
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from xgboost import XGBRegressor, XGBClassifier

from technews_nlp_aggregator.persistence.articles_similar_repo import ArticlesSimilarRepo


def print_best_parameters( classifier):
    if hasattr(classifier, "best_estimator_"):
        best_parameters = classifier.best_estimator_.get_params()
        for param_name in sorted(best_parameters.keys()):
            print("\t%s: %r" % (param_name, best_parameters[param_name]))


def create_regressor(train_DF, xboost_model_file):
    print(" ============= REGRESSOR ====================== ")
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


    clf = XGBRegressor(max_depth=5, min_child_weight=6, subsample=0.7,colsample_bytree=0.6,reg_alpha=0.001)
    clf.fit(X_train, y_train)
   # clf = XGBRegressor(min_child_weight=1,max_depth=3).fit(X_train,y_train)
    #print_best_parameters(clf)
    print("Training set : {} data points".format(len(X_train)))
    neg_mean_squared_error = cross_val_score(clf, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    print(neg_mean_squared_error )
    print("Neg Mean Squared Error: %0.8f (+/- %0.8f)" % (neg_mean_squared_error.mean(), neg_mean_squared_error .std() * 2))

    #neg_log_loss = cross_val_score(clf, X_train, y_train, cv=5, scoring='neg_log_loss')
   # print(neg_log_loss)
  #  print("Neg Log Loss: %0.8f (+/- %0.8f)" % (neg_log_loss.mean(), neg_log_loss.std() * 2))

    joblib.dump(clf, xboost_model_file)


def create_classifier(train_DF, xboost_classifier_file ):
    print(" ============= CLASSIFIER ===================== ")
  # train_df = pd.read_csv(train_file, index_col=0)
    relevant_columns = ['SCO_DAYS','SCO_D_TEXT', 'SCO_T_TEXT','SCO_D_TITLE',  'SCO_T_TITLE', 'SCO_T_SUMMARY', 'SCO_D_SUMMARY', 'SCO_T_SUMMARY_2', 'SCO_D_SUMMARY_2', 'SCO_CW_TITLE',  'SCO_CW_TEXT', 'SCO_CW_SUMMARY', 'SCO_CW_SUMMARY_2' ]

    result_columns = 'SCO_USER'
    X_train = np.array(train_df[relevant_columns])
    y_train = np.array(train_df[result_columns].map(lambda x: 1 if x > 0.8 else 0))
    xgbparams = {
        #'learning_rate':[ 0.001, 0.005, 0.01, 0.05, 0.1],
        #'n_estimators' : [100,200,500]
        #max_depth' : [2,3,4], 'min_child_weight' : [5,6,7]
        # 'min_child_weight' : [2,3,4], 'min_child_weight' : [5,6,7]
        #'colsample_bytree' : [0.6, 0.7, 0.8]
        #'reg_alpha' : [0, 0.1, 0.001, 0.0001]
        #'learning_rate' : [0.1, 0.01], 'n_estimators' : [100,200]

    }
    #clf =  GridSearchCV(XGBRegressor(max_depth=3, min_child_weight=6, gamma=0,colsample_bytree=0.8,subsample=0.8, reg_alpha=0.01, learning_rate=0.1), xgbparams)
    #clf =  GridSearchCV(XGBClassifier(), xgbparams)


    clf = XGBClassifier(max_depth=5, min_child_weight=6, subsample=0.7,colsample_bytree=0.6,reg_alpha=0.001)


   # clf = XGBClassifier()

    clf.fit(X_train, y_train)
   # clf = XGBRegressor(min_child_weight=1,max_depth=3).fit(X_train,y_train)
    f1 = cross_val_score(clf, X_train, y_train, cv=5, scoring='f1')


    f1 = cross_val_score(clf, X_train, y_train, cv=5, scoring='f1')
    precision = cross_val_score(clf, X_train, y_train, cv=5, scoring='precision')
    recall = cross_val_score(clf, X_train, y_train, cv=5, scoring='recall')


    accuracy = cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy')

    print_best_parameters(clf)
    print("Training set : {} data points".format(len(X_train)))
    print(f1)
    print("F1: %0.8f (+/- %0.8f)" % (f1.mean(), f1.std() * 2))
    print(precision)
    print("Precision: %0.8f (+/- %0.8f)" % (precision.mean(), precision.std() * 2))
    print(recall)
    print("Recall: %0.8f (+/- %0.8f)" % (recall.mean(), recall.std() * 2))
    print(accuracy)
    print("Accuracy: %0.8f (+/- %0.8f)" % (accuracy.mean(), accuracy.std() * 2))

    neg_log_loss = cross_val_score(clf, X_train, y_train, cv=5, scoring='neg_log_loss')
    print(neg_log_loss)
    print("Neg Log Loss: %0.8f (+/- %0.8f)" % (neg_log_loss.mean(), neg_log_loss.std() * 2))


    y_pred = clf.predict(X_train)

    train_df['SCO_PRED'] = y_pred


    joblib.dump(clf, xboost_classifier_file )


if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))
    db_config = yaml.safe_load(open(config["key_file"]))
    version = config["version"]
    db_url = db_config["db_url"]
    similarArticlesRepo = ArticlesSimilarRepo(db_url)
    train_df = similarArticlesRepo.load_train_set(version)
    xboost_model_file = config["root_dir"] + config["xgboost_model_file"]
    xboost_classifier_file = config["root_dir"] + config["xgboost_classifier_file"]

    create_regressor(train_df,  xboost_model_file)
    create_classifier(train_df, xboost_classifier_file)