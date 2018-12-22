

from sklearn.externals import joblib
import numpy as np
import yaml
import sys
from technews_nlp_aggregator.persistence.articles_similar_repo import  ArticlesSimilarRepo
from technews_nlp_aggregator.common import load_config
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



def predict(test_DF,  xboost_model_file, xboost_classif_file, predictions_df):
    print("setting index....")

    test_DF.set_index(['SCO_AIN_ID_1', 'SCO_AIN_ID_2'], inplace=True)
    print("removing already predicted....")

    merged_DF = test_DF[~test_DF.index.isin(predictions_df.index)]
    print("merged_df has {} rows".format(len(merged_DF )))

    relevant_columns = ['SCO_DAYS', 'SCO_W_DAYS', 'SCO_D_TEXT', 'SCO_T_TEXT','SCO_D_TITLE',  'SCO_T_TITLE', 'SCO_T_SUMMARY', 'SCO_D_SUMMARY', 'SCO_T_SUMMARY_2', 'SCO_D_SUMMARY_2', 'SCO_CW_TITLE',  'SCO_CW_TEXT', 'SCO_CW_SUMMARY', 'SCO_CW_SUMMARY_2' ]
    result_columns = 'SCO_USER'
    X_test = np.array(merged_DF[relevant_columns])
    clf = joblib.load(xboost_model_file)
    print("Regressor params")
    print(clf.get_params())

    y_test = clf.predict(X_test)
    merged_DF['SCO_REGR'] = y_test

    clf_clas = joblib.load(xboost_classif_file)
    print("Classifier params")
    print(clf_clas.get_params())

    y_clas = clf_clas.predict_proba(X_test)
    merged_DF['SCO_PROBA']  = y_clas[:,1]

    merged_DF.reset_index(drop=False, inplace=True)
    return merged_DF


if __name__ == '__main__':
    config_file = sys.argv[1] if (len(sys.argv) > 1) else 'config.yml'
    config = yaml.safe_load(open(config_file))

    version = config["version"]
    db_config = yaml.safe_load(open(config["key_file"]))
    db_url = db_config["db_url"]
    similarArticlesRepo = ArticlesSimilarRepo(db_url)


    version = config["version"]

    xboost_model_file = config["root_dir"] + config["xgboost_model_file"]
    xboost_classif_file = config["root_dir"] + config["xgboost_classifier_file"]

    test_df = similarArticlesRepo.load_test_set(version)
    print("Test_df has {} rows".format(len(test_df)))

    predictions_df = similarArticlesRepo.load_predictions(version)
    print("predictions_df has {} rows".format(len(predictions_df)))

    test_df_res = predict(test_df, xboost_model_file, xboost_classif_file, predictions_df)

    similarArticlesRepo.write_predictions(test_df_res, version)

