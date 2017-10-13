from gensim.models import Doc2Vec
from nltk.tokenize import word_tokenize

from technews_nlp_aggregator.nlp_model.publish.clf_facade import ClfFacade

MIN_FREQUENCY = 3


class Doc2VecFacade(ClfFacade):

    def __init__(self, model_filename, article_loader):
        self.model_filename = model_filename
        self.article_loader = article_loader


    def load_models(self):
        self.model = Doc2Vec.load(self.model_filename)


    def get_related_articles_and_sims(self, doc, n):
        wtok = [i for i in word_tokenize(doc.lower())]
        infer_vector = self.model.infer_vector(wtok)

        similar_documents = self.model.docvecs.most_similar([infer_vector], topn=n)

        return similar_documents


    def get_related_articles_and_score_doc(self, doc, n):

        return self.get_related_articles_and_sims(doc, n)


    def get_related_articles_and_sims_id(self, id, n):
        similar_documents = self.model.docvecs.most_similar([id], topn=n)[1:]

        return similar_documents

    def get_related_articles(self, doc, n, days=None):
        similar_documents = self.get_related_articles_and_sims(doc,n)

        urls = list(zip(*similar_documents))[0]

        return urls


    def get_related_articles_from_to(self, doc, max, start, end, n=10000):
        similar_documents = self.get_related_articles_and_score_doc(doc, n)
        id_articles, score_ids = zip(*similar_documents)
        articlesDocVecDf = self.article_loader.articlesDF.set_index('article_id',drop=True)
        articlesFoundDF = articlesDocVecDf .loc[list(id_articles), :]
        articlesFilteredDF = articlesFoundDF [( articlesFoundDF ['date_p'] >= start) & ( articlesFoundDF ['date_p'] <= end)]
        return articlesFilteredDF


    def get_related_articles_and_score_docid(self, docid, n=6000, max=15 ):
        docrow = self.article_loader.articlesDF[self.article_loader.articlesDF['article_id'] == docid]
        day = docrow ["date_p"]
        similar_documents = self.get_related_articles_and_sims_id(docid, n)
        df_similar_docs = self.enrich_with_score(similar_documents, 100)
        return df_similar_docs.iloc[:max, :]

    def interesting_articles_for_day(self, start, end, max=15):
        urls_of_day = self.article_loader.articles_in_interval(start, end)
        all_links = []
        for url in urls_of_day:
            ars_score = self.get_related_articles_and_score_url(url,6000,4)
            sum_score = sum([x[1] for x in ars_score])



            all_links.append((url, round(sum_score, 2),  [x[0] for x in ars_score]))
        sall_links = sorted(all_links, key = lambda x: x[1], reverse=True)[:max]
        return sall_links