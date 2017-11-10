import logging



from technews_nlp_aggregator.application import Application
import yaml
from math import log
def bow_w2v(application, n_articles=20 ):
    _ = application

    for i in range(n_articles):
        art_id1, art_id2 = _.similarArticlesRepo.retrieve_random_related()
        id1 = _.articleLoader.get_article(art_id1).index[0]

        id2 = _.articleLoader.get_article(art_id2).index[0]
        title1, text1 = _.articleLoader.articlesDF.iloc[id1]['title'], _.articleLoader.articlesDF.iloc[id1]['text']
        title2, text2 = _.articleLoader.articlesDF.iloc[id2]['title'],_.articleLoader.articlesDF.iloc[id2]['text']

        bow1 = _.tfidfFacade.corpus[id1]
        bow2 = _.tfidfFacade.corpus[id2]
        id2word = _.tfidfFacade.lsi.id2word
        tot_docs = len(_.tfidfFacade.corpus)
        common_words = [(w1,c1,c2) for w1, c1 in bow1 for w2,  c2 in bow2 if w1 == w2]
        bow_c = [
            (id2word[w1],
             w1,
             c1+c2,
             _.tfidfFacade.dictionary.dfs[w1],
             (c1 * log(tot_docs/_.tfidfFacade.dictionary.dfs[w1]),c2 * log(tot_docs/_.tfidfFacade.dictionary.dfs[w2])))
            for w1, c1 in bow1 for w2,  c2 in bow2 if w1 == w2 ]
        tfidf1 = [( id2word[w1], w1, c1 * log(tot_docs/_.tfidfFacade.dictionary.dfs[w1])) for w1, c1 in bow1 for w2,  c2 in bow2 if w1 == w2]

        tfidf2= [(id2word[w2], w2, c2 * log(tot_docs / _.tfidfFacade.dictionary.dfs[w2])) for w1, c1 in bow1 for w2, c2 in bow2 if w1 == w2 ]

        #bow_s = sorted(bow_c , key = lambda x: sum(x[4]), reverse=True)
        tfidf1_s = sorted([( id2word[w1], w1, c1 * log(tot_docs/_.tfidfFacade.dictionary.dfs[w1])) for w1, c1 in bow1 for w2,  c2 in bow2 if w1 == w2], key = lambda x: x[2], reverse=True)
        tfidf1_m = { id2word[w] : c1 * log(tot_docs/_.tfidfFacade.dictionary.dfs[w]) for w,c1,c2 in common_words}


        tfidf2_s= sorted([(id2word[w2], w2, c2 * log(tot_docs / _.tfidfFacade.dictionary.dfs[w2])) for w1, c1 in bow1 for w2, c2 in bow2 if w1 == w2 ], key = lambda x: x[2], reverse=True)
        tfidf2_m = {id2word[w]: c2 * log(tot_docs / _.tfidfFacade.dictionary.dfs[w]) for w, c1, c2 in common_words}


        avg_tfidf1 = sum(x[1] for x in tfidf1_m.items()) /  len(tfidf1_m.items())
        avg_tfidf2 = sum(x[1] for x in tfidf2_m.items()) /  len(tfidf2_m.items())
        sents_1_t = _.tokenizer.sentence_tokenizer.sent_tokenize(text1)
        sents_2_t = _.tokenizer.sentence_tokenizer.sent_tokenize(text2)

        sents_1 = select_sentences(_, avg_tfidf1, sents_1_t, tfidf1_m)
        sents_2 = select_sentences(_, avg_tfidf2, sents_2_t, tfidf2_m)

        print(" ============================= ")
        print(title1)
        for idx1, sent_1 in sents_1:
            print( '{} : {} '.format(idx1, sent_1) )

        print(" ============================= ")
        print(title2)
        for idx2, sent_2 in sents_2:
            print('{} : {} '.format(idx2, sent_2))


def select_sentences(_, avg_tfidf1, sents_t, tfidf1_m):
    sents_l = []
    seen_in_doc = []
    for idx, sent in enumerate(sents_t):
        mustAdd = False
        for token in _.tokenizer.tokenize_fulldoc(sent):


            if token in tfidf1_m and tfidf1_m[token] > avg_tfidf1 / 2 and token not in seen_in_doc:
                mustAdd = True
                seen_in_doc.append(token)
        if mustAdd:
            sents_l.append((1, sent))
        else:
            sents_l.append((0, sent))
    return sents_l


def bow_w2s(application, n_articles=20 ):
    _ = application

    for i in range(n_articles):
        id, article = _.articleLoader.get_random_article()
        title, text = article['title'], article['text']

        bow = _.tfidfFacade.corpus[id]
        id2word = _.tfidfFacade.lsi.id2word
        tot_docs = len(_.tfidfFacade.corpus)
        tfidf = sorted([( id2word[w], w, c * log(tot_docs/_.tfidfFacade.dictionary.dfs[w])) for w, c in bow], key=lambda x: x[2], reverse=True)


        tfidf_m = { id2word[w] : c * log(tot_docs/_.tfidfFacade.dictionary.dfs[w]) for w,c in bow}

        tfidf_left = sum_tfidf = sum(x[1] for x in tfidf_m.items())
        threshold = ((sum_tfidf) / 4) * 3
        tokens_to_keep = []
        tfidf_indx = 0
        while (tfidf_left > threshold ):
            tokens_to_keep.append(tfidf[tfidf_indx][0] )
            tfidf_indx += 1
            tfidf_left -= tfidf[tfidf_indx][2]
            print("Keeping {} : {}".format(tfidf[tfidf_indx][0], tfidf[tfidf_indx][2] ))


        sents_t = _.tokenizer.sentence_tokenizer.sent_tokenize(text)

        sents = select_sentences(_, tokens_to_keep, sents_t, tfidf_m)

        print(" ============================= ")
        print(title)
        for idx, sent in sents:
            print( '{} : {} '.format(idx, sent) )


def select_sentences(_, tok_to_keep, sents_t, tfidf1_m):
    print("TOKENS : {}".format(tok_to_keep))
    sents_l = []
    seen_in_doc = []
    for idx, sent in enumerate(sents_t):
        mustAdd = False
        for token in _.tokenizer.tokenize_fulldoc(sent):


            if token in tok_to_keep and token not in seen_in_doc:

                mustAdd = True
                seen_in_doc.append(token)
        if mustAdd:
            sents_l.append((1, sent))
        else:
            sents_l.append((0, sent))
    return sents_l



if __name__ == '__main__':
    config = yaml.safe_load(open('../../config.yml'))
    application = Application(config, True)
    bow_w2s(application)
