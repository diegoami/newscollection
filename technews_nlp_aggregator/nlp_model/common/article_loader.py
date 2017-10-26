
import logging
from random import randint
from . import exclude_articles
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



class ArticleLoader:


    def __init__(self, articlesRepo):
        self.articlesRepo = articlesRepo

    def get_random_article(self):
        url_len = len(self.articlesDF)
        rand_index = randint(0,url_len)
        return rand_index, self.articlesDF.loc[rand_index]

    def get_id_from_url(self, url):
        article_row = self.articlesDF[(self.articlesDF['url'] == url)]
        if (len(article_row) > 0):
            article_id = article_row.iloc[0]['article_id']
            return article_id
        else:
            return None

    def articles_in_interval(self,start, end):
        return self.articlesDF[(self.articlesDF['date_p'] >= start) & (self.articlesDF['date_p'] <= end) ]

    def load_all_articles(self, load_text=True, load_meta=True, limit=None):
        logging.info("Loading articles...")
        self.articlesDF =  self.articlesRepo.load_articles(load_text=True, load_meta=load_meta, limit=limit)

        self.articlesDF =  exclude_articles(self.articlesDF )
        if (not load_text):
            self.articlesDF.drop('text', inplace=True, axis=1)

        self.articlesDF.reset_index(inplace=True)
        self.tagsDF, self.articleTagsDF = self.articlesRepo.load_tags_tables()
        self.authorsDF, self.articleAuthorsDF = self.articlesRepo.load_authors_tables()

        return self.articlesDF

    def retrieve_meta(self, id):
        article_id = self.articlesDF.loc[id]['article_id']
        tags_of_article = self.articleTagsDF[self.articleTagsDF['article_id'] ==  article_id].merge(self.tagsDF,on='tag_id')
        tags_to_export = tags_of_article [['url','name']]
        authors_of_article =  self.articleAuthorsDF[self.articleAuthorsDF['article_id'] ==  id].merge(self.authorsDF, on='author_id')
        authors_to_export  = authors_of_article[['url','name']]
        return tags_to_export.to_dict(orient='records'), authors_of_article.to_dict(orient='records')
