import yaml

from technews_nlp_aggregator.persistence.similar_articles import  SimilarArticlesRepo

from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade, LsiInfo, TokenizeInfo, Doc2VecInfo, GramFacade

from technews_nlp_aggregator.summary.summary_facade import SummaryFacade

from technews_nlp_aggregator.nlp_model.common import ArticleLoader,  defaultTokenizer

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)




class Application:
    def __init__(self, config, load_text=False):
        db_config = yaml.safe_load(open(config["key_file"]))
        db_url = db_config["db_url"]
        self.load_text = load_text
        self.articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"), db_config.get("limit"))
        self.articleLoader = ArticleLoader(self.articleDatasetRepo)
        self.articleLoader.load_all_articles(load_text=load_text)
        self.similarArticlesRepo = SimilarArticlesRepo(db_url)
        self.gramFacade = GramFacade(config["phrases_model_dir_link"])
        self.tokenizer = defaultTokenizer
        self.doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], article_loader=self.articleLoader, gramFacade=self.gramFacade, tokenizer=defaultTokenizer  )
        self.doc2VecFacade.load_models()

        self.tfidfFacade = TfidfFacade(config["lsi_models_dir_link"], article_loader=self.articleLoader, gramFacade=self.gramFacade, tokenizer=defaultTokenizer  )
        self.tfidfFacade.load_models()

        self.lsiInfo = LsiInfo(self.tfidfFacade.lsi, self.tfidfFacade.corpus)
        self.tokenizeInfo = TokenizeInfo(self.tokenizer)
        self.doc2VecInfo = Doc2VecInfo(self.doc2VecFacade.model)
        self.summaryFacade = SummaryFacade(self.tfidfFacade, self.doc2VecFacade)

    def ensure_text_loaded(self):
        if (not self.load_text):
            self.articleLoader.load_all_articles(load_text=True)
            self.load_text = True

