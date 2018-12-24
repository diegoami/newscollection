import logging
from datetime import date


class ClassifierAggregator():

    def __init__(self, tokenizer, gramFacade, tfidfFacade, doc2VecFacade, tf2wv_mapper):
        self.tokenizer = tokenizer
        self.gramFacade = gramFacade
        self.tfidfFacade = tfidfFacade
        self.doc2VecFacade = doc2VecFacade
        self.tf2wv_mapper = tf2wv_mapper


    def retrieve_articles_for_text(self, text, start, end, n_articles, title, page_id):
        tdf_sims_map = self.retrieve_sims_map_with_dates(self.tfidfFacade, text=text, start=start, end=end,  title=title)
        doc2vec_sims_map = self.retrieve_sims_map_with_dates(self.doc2VecFacade, text=text, start=start, end=end,  title=title)
        #doc2vec_sims_map = self.retrieve_sims_map_with_dates(self.tf2wv_mapper, text=text, start=start, end=end, title=title)
        related_articles = self.merge_sims_maps(tdf_sims_map, doc2vec_sims_map, n_articles=n_articles, page_id=page_id)
        return related_articles

    def retrieve_articles_for_id(self, id, d_days, n_articles, page_id):
        tdf_sims_map = self.retrieve_sims_articles_for_id(self.tfidfFacade,  id=id, d_days=d_days   )
        doc2vec_sims_map = self.retrieve_sims_articles_for_id(self.doc2VecFacade, id=id, d_days=d_days    )
        related_articles = self.merge_sims_maps(tdf_sims_map, doc2vec_sims_map,
                                                n_articles=n_articles, page_id=page_id)
        return related_articles

    def merge_sims_maps(self,tdf_DF, doc2vec_DF, n_articles=100, page_id = 0):
        new_DF = tdf_DF.join(doc2vec_DF, lsuffix='_t', rsuffix='_d')
        new_DF['score_sums'] = ( new_DF['score_t'] + new_DF['score_d'] ) / 2
        new_DF.sort_values(by='score_sums', inplace=True, ascending=False)
        start, end = page_id * n_articles, (page_id + 1) * n_articles
        if (len(new_DF) > start):
            has_next = len(new_DF) > end
            new_DF = new_DF.iloc[start:min(end, len(new_DF))]
            return new_DF

        else:
            return None



    def retrieve_sims_map_with_dates(self, classifier, text, start=date.min, end=date.max,  title=''):
        scoresDF = classifier.get_related_articles_and_score_doc(doc=text, start=start, end=end, title=title)

        return scoresDF

    def retrieve_sims_articles_for_id(self, classifier, id, d_days):
        scoreDF = classifier.get_related_articles_for_id(id=id,  d_days=d_days)

        return scoreDF


    def missing_words(self, tok_doc):

        abs_words_gf = self.gramFacade.words_not_in_vocab(tok_doc, 100)
        abs_words_tf = self.tfidfFacade.get_absent_words(tok_doc)
        ins_word_gf = abs_words_gf.intersection(abs_words_tf)
        return ins_word_gf

    def common_miss_words_doc(self, tok1, tok2):
        mw_1, mw_2 = self.missing_words(tok1), self.missing_words(tok2)
        intw = mw_1.intersection(mw_2)
        logging.debug("Intersection words: {}".format(intw ))
        return len(mw_1.intersection(mw_2))



