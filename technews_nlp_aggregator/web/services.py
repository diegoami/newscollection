import yaml

from technews_nlp_aggregator.persistence.similar_articles import  SimilarArticlesRepo

from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.publish import Doc2VecFacade, TfidfFacade, LsiInfo, TokenizeInfo, Doc2VecInfo

from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer, TechArticlesTokenExcluder, SimpleTokenExcluder, TechArticlesWordTokenizer

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

config = yaml.safe_load(open('config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))
db_url    = db_config["db_url"]


class Application:
    def __init__(self):
        self.articleDatasetRepo = ArticleDatasetRepo(db_config.get("db_url"), db_config.get("limit"))
        self.articleLoader = ArticleLoader(self.articleDatasetRepo)
        self.articleLoader.load_all_articles(load_text=False)
        self.similarArticlesRepo = SimilarArticlesRepo(db_url)
        self.tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer(), word_tokenizer=TechArticlesWordTokenizer())
        self.doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], article_loader=self.articleLoader, tokenizer=self.tokenizer  )
        self.doc2VecFacade.load_models()

        self.tfidfFacade = TfidfFacade(config["lsi_models_dir_link"], article_loader=self.articleLoader, tokenizer=self.tokenizer   )
        self.tfidfFacade.load_models()

        self.lsiInfo = LsiInfo(self.tfidfFacade.lsi, self.tfidfFacade.corpus)
        self.tokenizeInfo = TokenizeInfo(self.tokenizer)
        self.doc2VecInfo = Doc2VecInfo(self.doc2VecFacade.model)


