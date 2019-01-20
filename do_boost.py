import yaml
from datetime import datetime
import logging
import os
from technews_nlp_aggregator.persistence.articles_similar_repo import ArticlesSimilarRepo
from technews_nlp_aggregator.persistence.model_repo import ModelRepo
from technews_nlp_aggregator.model.xgboost_fit import create_classifier as xgb_create_classifier
from technews_nlp_aggregator.model.xgboost_fit import create_regressor as xgb_create_regressor
from technews_nlp_aggregator.model.rtf_fit import create_classifier as rtf_create_classifier
from technews_nlp_aggregator.model.rtf_fit import create_regressor as rtf_create_regressor
from technews_nlp_aggregator.model.sgd_fit import create_classifier as sgd_create_classifier
from technews_nlp_aggregator.model.sgd_fit import create_regressor as sgd_create_regressor

from technews_nlp_aggregator.model.scoring import threshold_scores_clf, cross_val_score_clf, cross_val_score_regr, \
    feature_importances, mean_scores_clf, mean_scores_regr, loop_threshold_scores
from technews_nlp_aggregator.model.visualization import map_threshold

import sys
from sklearn.externals import joblib

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def model_workflow(model_name, db_config, train_df, threshold, clf_method, regr_method):

    def calc_scoring(df, clf, reg, threshold, model_name):

        clf_scores = cross_val_score_clf(clf, df)
        regr_scores = cross_val_score_regr(reg, df)
        threshold_scores = threshold_scores_clf(clf, df, threshold=threshold)
        loop_threshold_scores(df, clf)
        map_threshold(df, clf, model_name=model_name)
        return  {"clf": clf_scores, "regr" : regr_scores, "threshold" : threshold_scores }


    def fill_model(scores):
        training_model = {}
        training_model["TMO_TRAINING_SET"] = len(train_df)
        training_model["TMO_DATE"] = datetime.now()
        training_model.update(scores["threshold"])
        training_model.update(scores["regr"])
        training_model["TMO_YCLF_MEAN"] = mean_scores_clf(train_df)
        training_model["TMO_YREG_MEAN"] = mean_scores_regr(train_df)
        return training_model


    def save_to_model(model_repo, training_model, clf, reg):
        training_model["TMO_NAME"] = "model_repo"
        model_repo.save_model_performance(training_model)
        model_repo.save_feature_report('R', feature_importances(reg))
        model_repo.save_feature_report('C', feature_importances(clf))


    def save_model_to_file(name, config, clf, reg):
        os.makedirs(config["root_dir"] + config["{}_model_dir".format(name)], exist_ok=True)
        model_file = config["root_dir"] + config["{}_model_file".format(name)]
        classifier_file = config["root_dir"] + config["{}_classifier_file".format(name)]
        joblib.dump(clf, classifier_file)
        joblib.dump(reg, model_file)


    logging.info("======================================================")
    logging.info("======================== {} ====================".format(model_name))
    logging.info("======================================================")
    clf = clf_method(train_df)
    reg = regr_method(train_df)
    scores = calc_scoring(df=train_df, clf=clf, reg=reg, threshold=threshold, model_name=model_name)
    training_model = fill_model(scores)
    model_repo = ModelRepo(db_config["db_url"])
    save_to_model(model_repo, training_model, clf, reg)
    save_model_to_file(model_name, config, clf, reg)
    logging.info("======================================================")
    logging.info("======================================================")

if __name__ == '__main__':
    config_file = sys.argv[1] if (len(sys.argv) > 1) else 'config.yml'
    config = yaml.safe_load(open(config_file))
    db_config = yaml.safe_load(open(config["key_file"]))

    similarArticlesRepo = ArticlesSimilarRepo(db_config["db_url"], group_limit=config.get("group_limit",20000),
                                              list_limit=config.get("list_limit",5000))
    train_df = similarArticlesRepo.load_train_set(config["version"])
    threshold = config.get("threshold", 0.65)


    #model_workflow("xgboost", db_config, train_df, threshold, xgb_create_classifier, xgb_create_regressor)
    #model_workflow("rtf", db_config, train_df.fillna(0), threshold, rtf_create_classifier, rtf_create_regressor)
    model_workflow("sgd", db_config, train_df.fillna(0), threshold, sgd_create_classifier, sgd_create_regressor)