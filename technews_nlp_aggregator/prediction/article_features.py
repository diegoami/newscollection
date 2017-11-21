import logging


class ArticleFeatures:
    def __init__ (self, id, article_id, article):
        self.id = id
        self.article_id = article_id
        self.article = article

    def retrieve_tokens(self, tfidfFacade):
        self.tokenized_title = tfidfFacade.get_tokenized(doc=self.article['title'])
        self.tokenized_summary =   self.tokenized_title + tfidfFacade.get_tokenized(doc=self.summary)
        self.tokenized_summaryb = self.tokenized_title + tfidfFacade.get_tokenized(doc=self.summaryb)
        self.tokenized_full_text = self.tokenized_title + tfidfFacade.get_tokenized(doc=self.article['text'])

    def retrieve_summaries(self, summaryFacade):

        self.summary = summaryFacade.full_text_summarize(id=self.id, doc=self.article['text'], title=self.article['title'], threshold=0.85)
        self.summaryb = summaryFacade.full_text_summarize(id=self.id, doc=self.article['text'], title=self.article['title'], threshold=0.7)





