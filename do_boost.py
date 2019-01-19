import yaml
from datetime import datetime
import logging
import os
from technews_nlp_aggregator.persistence.articles_similar_repo import ArticlesSimilarRepo
from technews_nlp_aggregator.persistence.model_repo import ModelRepo
from technews_nlp_aggregator.model.xgboost_fit import create_classifier, create_regressor
from technews_nlp_aggregator.model.scoring import threshold_scores_clf, cross_val_score_clf, cross_val_score_regr, \
    feature_importances, mean_scores_clf, mean_scores_regr, loop_threshold_scores
from technews_nlp_aggregator.model.visualization import map_threshold

import sys
from sklearn.externals import joblib

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
training_model = {}


if __name__ == '__main__':
    config_file = sys.argv[1] if (len(sys.argv) > 1) else 'config.yml'
    config = yaml.safe_load(open(config_file))

    db_config = yaml.safe_load(open(config["key_file"]))
    threshold = config.get("threshold", 0.65)
    similarArticlesRepo = ArticlesSimilarRepo(db_config["db_url"], group_limit=config.get("group_limit",20000),
                                              list_limit=config.get("list_limit",5000))
    modelRepo = ModelRepo(db_config["db_url"])
    os.makedirs(config["root_dir"] + config["xgboost_model_dir"], exist_ok=True)

    xboost_model_file = config["root_dir"] + config["xgboost_model_file"]
    xboost_classifier_file = config["root_dir"] + config["xgboost_classifier_file"]
    train_df = similarArticlesRepo.load_train_set(config["version"])

    training_model["TMO_TRAINING_SET"] = len(train_df)
    training_model["TMO_DATE"] = datetime.now()

    clf  = create_classifier(train_df)
    joblib.dump(clf, xboost_classifier_file)

    regressor = create_regressor(train_df)
    joblib.dump(regressor, xboost_model_file)

    clf_scores = cross_val_score_clf(clf, train_df)
    regr_scores = cross_val_score_regr(regressor, train_df)
    threshold_scores = threshold_scores_clf(clf, train_df, threshold=threshold)

    training_model.update(threshold_scores)
    training_model.update(regr_scores )

    training_model["TMO_YCLF_MEAN"] = mean_scores_clf(train_df)
    training_model["TMO_YREG_MEAN"] = mean_scores_regr(train_df)


    modelRepo.save_model_performance(training_model)
    modelRepo.save_feature_report('R', feature_importances(clf ))
    modelRepo.save_feature_report('C', feature_importances(regressor ))

    loop_threshold_scores(train_df, clf)

    map_threshold(train_df, clf)