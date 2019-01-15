import yaml
from datetime import datetime
import logging
import os
from technews_nlp_aggregator.persistence.articles_similar_repo import ArticlesSimilarRepo
from technews_nlp_aggregator.persistence.model_repo import ModelRepo
from technews_nlp_aggregator.prediction.model import create_classifier, create_regressor, map_threshold
import sys

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
training_model = {}


if __name__ == '__main__':
    config_file = sys.argv[1] if (len(sys.argv) > 1) else 'config.yml'
    config = yaml.safe_load(open(config_file))

    db_config = yaml.safe_load(open(config["key_file"]))
    similarArticlesRepo = ArticlesSimilarRepo(db_config["db_url"], group_limit=config.get("group_limit",20000),
                                              list_limit=config.get("list_limit",5000))
    modelRepo = ModelRepo(db_config["db_url"])
    os.makedirs(config["root_dir"] + config["xgboost_model_dir"], exist_ok=True)

    xboost_model_file = config["root_dir"] + config["xgboost_model_file"]
    xboost_classifier_file = config["root_dir"] + config["xgboost_classifier_file"]
    train_df = similarArticlesRepo.load_train_set(config["version"])

    training_model["TMO_TRAINING_SET"] = len(train_df)
    training_model["TMO_DATE"] = datetime.now()

    clf, clf_model_returned, clf_feature_report, clf_best_params  = create_classifier(train_df, xboost_classifier_file)
    map_threshold(train_df, clf)
    clf, regr_model_returned, regr_feature_report, regr_best_params = create_regressor(train_df, xboost_model_file)


    training_model.update(clf_model_returned)
    training_model.update(regr_model_returned)

    modelRepo.save_model_performance(training_model)
    modelRepo.save_feature_report('R', regr_feature_report)
    modelRepo.save_feature_report('C', clf_feature_report)