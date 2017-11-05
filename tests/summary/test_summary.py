import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, defaultTokenizer, TechArticlesSentenceTokenizer,  TechArticlesWordTokenizer

from technews_nlp_aggregator.nlp_model.publish import TfidfFacade, Doc2VecFacade, GramFacade
import yaml


from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
from technews_nlp_aggregator.summary import SummaryFacade
import yaml

config = yaml.safe_load(open('../../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)
gramFacade = GramFacade(config["phrases_model_dir_link"])
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader, gramFacade, defaultTokenizer)
tfidfFacade.load_models()
doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader, gramFacade, defaultTokenizer)
doc2VecFacade.load_models()
summaryFacade = SummaryFacade(tfidfFacade , doc2VecFacade)
for _ in range(20):

    random_article_id, random_article = articleLoader.get_random_article()
    #random_article_id = 15073
    random_article_url = random_article ['url']
    # print(random_article)
    print(" ============= ARTICLE ==================")
    title, text = random_article["title"], random_article["text"]
    print(title)
    print(text)

    print(" ============= SUMMARY ==================")
    summary_sentences = summaryFacade.summarize(title, text, random_article_id, 90)
    print(title)
    for summary_sentence in summary_sentences:
        print(summary_sentence)
