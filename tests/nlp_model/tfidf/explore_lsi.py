import logging

import yaml
from technews_nlp_aggregator.application import Application
from random import randint

def show_topics(application):
    _ = application
    for topicno in range(_.lsiInfo.num_topics):
        print(" ================= TOPIC {} =======================".format(topicno))
        topic_values = _.lsi_info.get_topic_no_array(topicno)
        for word, value in topic_values:
            if (abs(value) > 0.01):
                print(word, value)

def analize_bows(icorp, _ ):
    i_bow = _.lsi_info.corpus[icorp]
    i_words_docid = _.lsiInfo.get_words_docid(icorp)
    i_topics_docid = _.lsiInfo.get_topics_docid(icorp)
    print(i_bow)
    print(i_words_docid)
    print(i_topics_docid)
    list_words = []
    for word, count in i_bow:
        bow_single = [(word, count)]
        smodel = _.lsi_info.model[bow_single]
        topicsum = sum([abs(x[1]) for x in smodel])
        list_words.append((_.lsiInfo.id2word[word], topicsum))
    slist_words = sorted(list_words, key=lambda x: x[1], reverse=True)
    print(slist_words)

def analize_article(application):
    _ = application
    for i in range(10):
        print("ARTICLE {} ".format(i))
        icorp = randint(0,len(_.lsi_info.corpus))
        analize_bows(icorp, _ )
        doc = _.articleLoader.articlesDF.iloc[icorp]["text"]
        sentences_tokenizer = _.tokenizer.sentence_tokenizer
        for sentence in sentences_tokenizer.sent_tokenize(doc):
            scores = _.tfidfFacade.compare_docs_to_id(sentence, icorp)
            print(sentence)
            print(scores)

if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    show_topics(application)


