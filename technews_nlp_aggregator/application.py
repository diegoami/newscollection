import yaml

from technews_nlp_aggregator.persistence.similar_articles import  SimilarArticlesRepo

from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade, LsiInfo, TokenizeInfo, Doc2VecInfo, GramFacade

from technews_nlp_aggregator.summary.summary_facade import SummaryFacade

from technews_nlp_aggregator.nlp_model.common import ArticleLoader,  defaultTokenizer

import logging




class Application:
    def __init__(self, config, load_text=False):
        self.db_config = yaml.safe_load(open(config["key_file"]))
        self.db_url = self.db_config["db_url"]
        self.load_text = load_text
        self.articleDatasetRepo = ArticleDatasetRepo(self.db_config.get("db_url"), self.db_config.get("limit"))
        self.articleLoader = ArticleLoader(self.articleDatasetRepo)
        self.articleLoader.load_all_articles(load_text=load_text)
        self.similarArticlesRepo = SimilarArticlesRepo(self.db_url)
        self.tokenizer = defaultTokenizer
        self.gramFacade = GramFacade(config["phrases_model_dir_link"])
        self.gramFacade.load_models()

        self.doc2VecFacade = Doc2VecFacade(config["doc2vec_models_dir_link"], article_loader=self.articleLoader, gramFacade=self.gramFacade, tokenizer=defaultTokenizer  )
        self.doc2VecFacade.load_models()

        self.tfidfFacade = TfidfFacade(config["lsi_models_dir_link"], article_loader=self.articleLoader, gramFacade=self.gramFacade, tokenizer=defaultTokenizer  )
        self.tfidfFacade.load_models()

        self.lsiInfo = LsiInfo(self.tfidfFacade.lsi, self.tfidfFacade.corpus)
        self.tokenizeInfo = TokenizeInfo(self.tokenizer)
        self.doc2VecInfo = Doc2VecInfo(self.doc2VecFacade.model)
        self.summaryFacade = SummaryFacade(self.tfidfFacade, self.doc2VecFacade)
        last_article_date = self.articleDatasetRepo.get_latest_article_date()

        self.latest_article_date = str(last_article_date.year) + '-' + str(last_article_date.month) + '-' + str(last_article_date.day)
        logging.debug("Log in debug mode")


    def ensure_text_loaded(self):
        if (not self.load_text):
            self.articleLoader.load_all_articles(load_text=True)
            self.load_text = True

    def reload(self):
        self.articleLoader.load_all_articles(load_text=True)
        self.gramFacade.load_models()
        self.doc2VecFacade.load_models()
        self.tfidfFacade.load_models()

