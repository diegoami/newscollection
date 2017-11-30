import yaml

from technews_nlp_aggregator.application import Application


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


if __name__ == '__main__':
    config = yaml.safe_load(open('../../../config.yml'))
    application = Application(config, True)
    show_topics(application)


