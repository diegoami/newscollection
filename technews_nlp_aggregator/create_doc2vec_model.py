import logging
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.nlp_model.generation import Doc2VecGenerator
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer, TechArticlesTokenExcluder, SimpleTokenExcluder
from datetime import datetime
import yaml

import yaml

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(load_text=True, load_meta=False)
tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer(), token_excluder=SimpleTokenExcluder())


models_dir = config["doc2vec_models_dir_base"] + datetime.now().isoformat()+'/'

os.mkdir(models_dir)

doc2VecGenerator = Doc2VecGenerator(articleLoader.articlesDF , models_dir, tokenizer)
doc2VecGenerator.create_model()

if os.path.islink(config["doc2vec_models_dir_link"]):
    os.unlink(config["doc2vec_models_dir_link"])
os.symlink(models_dir,config["doc2vec_models_dir_link"])
