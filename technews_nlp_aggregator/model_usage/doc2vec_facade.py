from gensim.models import Doc2Vec
from nltk.tokenize import word_tokenize

from technews_nlp_aggregator.model_usage.clf_facade import ClfFacade

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

    def get_related_articles(self, doc, n, days=None):
        similar_documents = self.get_related_articles_and_sims(doc,n)

        urls = list(zip(*similar_documents))[0]

        return urls

    def get_related_articles_and_score(self,  urlArg , n=5000, max=15):
        orig_record = self.article_loader.article_map[urlArg ]
        day = orig_record ["date_p"]
        orig_text = orig_record ["text"]

        similar_documents = self.get_related_articles_and_sims(orig_text , n)
        rated_urls = []

        for url, score in similar_documents:
            if (url == urlArg):
                continue

            record = self.article_loader.article_map[url]

            p_date = record["date_p"]
            real_score = score * 125-abs(p_date-day).days

            if (record["source"] == orig_record["source"]):
                real_score -= 5

            if (real_score > 0):
                rated_urls.append((url,real_score))

        srated_urls = sorted(rated_urls, key=lambda x: x[1],reverse=True)
        return srated_urls[:max]
