import yaml

from technews_nlp_aggregator.persistence.articles_similar_repo import  ArticlesSimilarRepo

from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade, LsiInfo, TokenizeInfo, Doc2VecInfo, GramFacade, ClassifierAggregator

from technews_nlp_aggregator.summary.summary_facade import SummaryFacade

from technews_nlp_aggregator.nlp_model.common import ArticleLoader,  defaultTokenizer, ArticleSimilarLoader

import logging


from datetime import date

class Application:
    def __init__(self, config, load_text=False):
        self.db_config = yaml.safe_load(open(config["key_file"]))
        self.db_url = self.db_config["db_url"]
        self.load_text = load_text
        self.articleDatasetRepo = ArticleDatasetRepo(self.db_config.get("db_url"))
        self.articleLoader = ArticleLoader(self.articleDatasetRepo)
        self.articleLoader.load_all_articles(load_text=load_text)
        self.similarArticlesRepo = ArticlesSimilarRepo(self.db_url)

        self.articleSimilarLoader = ArticleSimilarLoader(self.similarArticlesRepo, config["train_data_file_aug"])
        self.tokenizer = defaultTokenizer
        self.gramFacade = GramFacade(config["phrases_model_dir_link"])
        self.gramFacade.load_models()

        self.doc2VecFacade = Doc2VecFacade(config["doc2vec_models_dir_link"], article_loader=self.articleLoader, gramFacade=self.gramFacade, tokenizer=defaultTokenizer  )
        self.doc2VecFacade.load_models()

        self.tfidfFacade = TfidfFacade(config["lsi_models_dir_link"], article_loader=self.articleLoader, gramFacade=self.gramFacade, tokenizer=defaultTokenizer  )
        self.tfidfFacade.load_models()

        self.lsiInfo = LsiInfo(self.tfidfFacade.lsi, self.tfidfFacade.corpus)
        self.tokenizeInfo = TokenizeInfo(self.tokenizer)
        self.doc2VecInfo = Doc2VecInfo(self.doc2VecFacade.model, self.doc2VecFacade)
        self.summaryFacade = SummaryFacade(self.tfidfFacade, self.doc2VecFacade)
        self.classifierAggregator = ClassifierAggregator(self.tokenizer, self.gramFacade, self.tfidfFacade, self.doc2VecFacade)
        last_article_date = self.articleDatasetRepo.get_latest_article_date()

        self.latest_article_date = str(last_article_date.year) + '-' + str(last_article_date.month) + '-' + str(last_article_date.day)
        self.threshold = config["threshold"]
        self.refresh_groups()
        logging.debug("Log in debug mode")


    def ensure_text_loaded(self):
        if (not self.load_text):
            self.articleLoader.load_all_articles(load_text=True)
            self.load_text = True

    def reload(self):
        self.articleLoader.load_all_articles(load_text=True)


    def verify_acceptable_article(self, text, title):

        articles_similar = self.classifierAggregator.retrieve_articles_for_text(text, date.min, date.max, 6, title, 0 )
        art_df = articles_similar .join(self.articleLoader.articlesDF)
        sources = art_df['source'].unique()
        return (len(sources) > 1)

    def refresh_groups(self):
        all_groups_list = self.articleSimilarLoader.retrieve_groups(articleLoader=self.articleLoader, threshold=self.threshold)
        self.article_groups = []
        for group in all_groups_list:

            articlesDF = self.articleLoader.articlesDF
            articles_in_groupDF = articlesDF[articlesDF['article_id'].isin(group)]
            articles = []
            article_ids = articles_in_groupDF['article_id'].tolist()

            for id, row in articles_in_groupDF.iterrows():
                article = {
                    "article_id": row['article_id'],
                    "title": row['title'],
                    "date": row['date_p'],
                    "url": row['url'],
                    "source": row['source'],
                    "other_ids": [article_id for article_id in article_ids if article_id != row['article_id']]
                }
                articles.append(article)
            self.article_groups.append(
                {"articles": articles, "article_list": "-".join([str(article["article_id"]) for article in articles])})
        self.article_groups.sort(key=lambda article_group: article_group["articles"][0]["date"], reverse=True)