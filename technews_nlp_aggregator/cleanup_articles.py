import sys
sys.path.append('..')
import yaml

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, TechArticlesSentenceTokenizer, TechArticlesCleaner
from nltk.tokenize import sent_tokenize

config = yaml.safe_load(open('../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))
db_url    = db_config["db_url"]
articleDatasetRepo = ArticleDatasetRepo(db_url)
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)

sentence_tokenizer = TechArticlesSentenceTokenizer()
article_cleaner    = TechArticlesCleaner()

def save_cleaned_text(row):
    text = row["text"]
    article_id = row["article_id"]
    text = article_cleaner.do_clean(text)
    text = sentence_tokenizer.clean_sentences(text)
#    print(text)
    articleDatasetRepo.update_article_text(article_id, "\n".join(text))
    return row

articleFilteredDF = articleLoader.articlesDF[:100]
articleFilteredDF.apply(save_cleaned_text, axis=1)






