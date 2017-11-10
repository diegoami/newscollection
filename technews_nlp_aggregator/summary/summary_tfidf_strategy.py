from math import log
import logging

class SummaryTfidfStrategy():
    def __init__(self,  tfidfFacade, threshold_mult=0.8):
        self.tfidfFacade = tfidfFacade
        self.threshold_mult = threshold_mult

    def get_summary_sentences(self, id, text):

        bow = self.tfidfFacade.corpus[id]
        return self.get_sentences_from_bow(bow, text)

    def get_sentences_from_bow(self, bow, text):
        id2word = self.tfidfFacade.lsi.id2word
        tot_docs = len(self.tfidfFacade.corpus)
        tfidf = sorted([(id2word[w], w, c * log(tot_docs / self.tfidfFacade.dictionary.dfs[w])) for w, c in bow],
                       key=lambda x: x[2], reverse=True)
        tfidf_m = {id2word[w]: c * log(tot_docs / self.tfidfFacade.dictionary.dfs[w]) for w, c in bow}
        tfidf_left = sum_tfidf = sum(x[1] for x in tfidf_m.items())
        logging.debug("SUMTFIDF : {}".format(round(sum_tfidf)))
        threshold = sum_tfidf * self.threshold_mult
        logging.debug("THRESHOLD: {}".format(round(threshold)))
        tokens_to_keep = []
        tfidf_indx = 0
        while (tfidf_left > threshold):
            tokens_to_keep.append(tfidf[tfidf_indx][0])
            tfidf_indx += 1
            tfidf_left -= tfidf[tfidf_indx][2]
            logging.debug(" Adding {} for {} : left {}".format(tfidf[tfidf_indx][0], tfidf[tfidf_indx][2], tfidf_left))
        sents_t = self.tfidfFacade.tokenizer.sentence_tokenizer.sent_tokenize(text)
        sents = self.select_sentences(tokens_to_keep, sents_t, tfidf_m)
        return sents

    def select_sentences(self, tok_to_keep, sents_t, tfidf1_m):
        logging.debug("Trying to match {}".format(tok_to_keep))
        sents_l = []
        seen_in_doc = []
        for idx, sent in enumerate(sents_t):
            mustAdd = False
            seen_in_sent = []
            for token in self.tfidfFacade.get_tokenized(doc=sent):

                if token in tok_to_keep:
                    seen_in_sent.append(token)
                    if token not in seen_in_doc:

                        mustAdd = True
                        seen_in_doc.append(token)
            logging.debug("{} : {} ".format(str(idx), str(seen_in_sent)))
            if mustAdd:
                sents_l.append((1, sent))

            else:
                sents_l.append((0, sent))

        return sents_l

