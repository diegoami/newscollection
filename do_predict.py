

import yaml
import sys
from technews_nlp_aggregator.persistence.articles_similar_repo import  ArticlesSimilarRepo
from technews_nlp_aggregator.prediction.xgboost_fit import predict
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)




if __name__ == '__main__':
    config_file = sys.argv[1] if (len(sys.argv) > 1) else 'config.yml'
    config = yaml.safe_load(open(config_file))


    db_config = yaml.safe_load(open(config["key_file"]))
    similarArticlesRepo = ArticlesSimilarRepo(db_config["db_url"], group_limit=config.get("group_limit",20000),
                                              list_limit=config.get("list_limit",5000))

    xboost_model_file = config["root_dir"] + config["xgboost_model_file"]
    xboost_classif_file = config["root_dir"] + config["xgboost_classifier_file"]

    test_df = similarArticlesRepo.load_test_set(version = config["version"])
    logging.info("Test_df has {} rows".format(len(test_df)))

    predictions_df = similarArticlesRepo.load_predictions(config["version"])
    logging.info("predictions_df has {} rows".format(len(predictions_df)))

    test_df_res = predict(test_df, xboost_model_file, xboost_classif_file, predictions_df)
    logging.info("Preparing to write {} predictions".format(len(test_df_res)))
    num_predictions = similarArticlesRepo.write_predictions(test_df_res, config["version"])
    logging.info("{} predictions done".format(num_predictions))

