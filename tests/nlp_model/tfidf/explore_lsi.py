import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader, defaultTokenizer
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade, LsiInfo, GramFacade
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
articleLoader.load_all_articles(True)
gramFacade = GramFacade(config["phrases_model_dir_link"])
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader, gramFacade )
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


def analizye_bows():
    i_bow = lsi_info.corpus[icorp]
    i_words_docid = lsi_info.get_words_docid(icorp)
    i_topics_docid = lsi_info.get_topics_docid(icorp)
    print(i_bow)
    print(i_words_docid)
    print(i_topics_docid)
    list_words = []
    for word, count in i_bow:
        bow_single = [(word, count)]
        smodel = lsi_info.model[bow_single]
        topicsum = sum([abs(x[1]) for x in smodel])
        list_words.append((lsi_info.id2word[word], topicsum))
    slist_words = sorted(list_words, key=lambda x: x[1], reverse=True)
    print(slist_words)


for i in range(10):
    print("ARTICLE {} ".format(i))
    icorp = randint(0,len(lsi_info.corpus))
    #analizye_bows()
    doc = articleLoader.articlesDF.iloc[icorp]["text"]
    sentences_tokenizer = defaultTokenizer.sentence_tokenizer
    for sentence in sentences_tokenizer.process('', doc):
        scores = tfidfFacade.compare_docs_to_id(sentence, icorp)
        print(sentence)
        print(scores)









