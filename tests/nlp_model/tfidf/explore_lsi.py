import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade, LsiInfo
import yaml


from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.generation import TfidfGenerator
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from datetime import datetime
import yaml

config = yaml.safe_load(open('../../../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(False)
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader)
tfidfFacade.load_models()
lsi_info = LsiInfo(tfidfFacade.lsi, tfidfFacade.corpus)


def show_topics():
    for topicno in range(lsi_info.num_topics):
        print(" ================= TOPIC {} =======================".format(topicno))
        topic_values = lsi_info.get_topic_no_array(topicno)
        for word, value in topic_values:
            if (abs(value) > 0.01):
                print(word, value)
from random import randint
for i in range(100):
    icorp = randint(0,len(lsi_info.corpus))
    i_words_docid, i_topics_docid = lsi_info.get_words_docid(icorp), lsi_info.get_topics_docid(icorp)
    print(i_words_docid, i_topics_docid )

    jcorp = randint(0,len(lsi_info.corpus))
    j_words_docid, j_topics_docid = lsi_info.get_words_docid(jcorp), lsi_info.get_topics_docid(jcorp)









