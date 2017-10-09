MIN_FREQUENCY = 3
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'

import logging

from gensim import corpora, models, similarities
from gensim.corpora import MmCorpus
from nltk.tokenize import word_tokenize

from technews_nlp_aggregator.model_usage.clf_facade import ClfFacade

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class TfidfFacade(ClfFacade):

    def __init__(self, model_dir, article_loader):
        self.model_dir = model_dir
        self.article_loader = article_loader

    def load_models(self):
        self.dictionary = corpora.Dictionary.load(self.model_dir + '/'+DICTIONARY_FILENAME)  # store the dictionary, for future reference
        self.corpus = MmCorpus(self.model_dir + '/'+ CORPUS_FILENAME )
        self.lsi = models.LsiModel.load(self.model_dir + '/'+ LSI_FILENAME)
        self.index = similarities.MatrixSimilarity.load(self.model_dir + '/'+ INDEX_FILENAME)  # transform corpus to LSI space and index it


    def get_vec(self,doc):
        words = [word for word in word_tokenize(doc.lower())]
        vec_bow = self.dictionary.doc2bow(words)
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def get_vec_docid(self, id):

        vec_bow = self.corpus[id]
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def get_related_sims_docid(self, id, n):
        vec_lsi = self.get_vec_docid(id)
        sims = self.index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return sims[1:n]


    def get_related_sims(self, doc, n):
        vec_lsi = self.get_vec(doc)
        sims = self.index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return sims[:n]

    def get_related_articles(self, doc, n):
        sims = self.get_related_sims(doc,n)
        article_map = self.article_loader.article_map
        url_list = self.article_loader.url_list
        urls= [url_list[sim[0]] for sim in sims]
        return urls[:n]

    def get_related_articles_and_score_doc(self, doc, n):
        sims = self.get_related_sims(doc, n)

        article_map = self.article_loader.article_map
        url_list = self.article_loader.url_list
        related_articles = list(zip([url_list[sim[0]] for sim in sims],[sim[1] for sim in sims]))

        return related_articles[:n]

    def get_related_articles_and_score_docid(self,  docid, n=6000, max=15):
        urlArg = self.article_loader.url_list[docid]
        orig_record = self.article_loader.article_map[
            urlArg
        ]
        day = orig_record ["date_p"]
        similar_documents = self.get_related_sims_docid(docid, n)
        rated_urls = []

        for index, score in similar_documents:
            url = self.article_loader.url_list[index]
            if (url == urlArg):
                continue

            record = self.article_loader.article_map[url]
            if (day == None):
                day = record["date_p"]


            p_date = record["date_p"]
            real_score = score * 100 - abs(p_date - day).days
           # str_exp = str(round(score, 2)) + "*100-" + str(abs(p_date - day).days)
            if (record["source"] == orig_record["source"]):
                real_score -= 5
               # str_exp = str_exp + "-5"
            if (real_score > 0):
                rated_urls.append((url, real_score ))

        srated_urls = sorted(rated_urls, key=lambda x: x[1], reverse=True)
        return srated_urls[:max]

    def interesting_articles_for_day(self, start, end, max=15):
        docs_of_day = self.article_loader.docs_in_interval(start, end)
        all_links = []
        for docid in docs_of_day:
            ars_score = self.get_related_articles_and_score_docid(docid, 6000, 4)
            sum_score = sum([x[1] for x in ars_score])
            url = self.article_loader.url_list[docid]


            all_links.append((url, round(sum_score, 2), [x[0] for x in ars_score]))
        sall_links = sorted(all_links, key=lambda x: x[1], reverse=True)[:max]
        return sall_links