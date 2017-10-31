import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.nlp_model.common import ArticleLoader, DefaultTokenizer, TechArticlesSentenceTokenizer, TechArticlesTokenExcluder, SimpleTokenExcluder, NltkWordTokenizer

from technews_nlp_aggregator.nlp_model.publish import TfidfFacade, Doc2VecFacade
import yaml


from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
import yaml

config = yaml.safe_load(open('../../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))
tokenizer = DefaultTokenizer(sentence_tokenizer=TechArticlesSentenceTokenizer(),
                                 token_excluder=TechArticlesTokenExcluder(),
                             word_tokenizer=NltkWordTokenizer())
articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(True)
tfidfFacade   = TfidfFacade(config["lsi_models_dir_link"], articleLoader, tokenizer)
tfidfFacade.load_models()
doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader, tokenizer)
doc2VecFacade.load_models()
while True:

    random_article_id, random_article = articleLoader.get_random_article()
    #random_article_id = 15073
    random_article_url = random_article ['url']
    # print(random_article)
    print(" ============= ARTICLE ==================")
    print(random_article["title"])
    print("\n".join(tokenizer.sentence_tokenizer.clean_sentences(random_article["text"])))


   # print(" ============= DOC2VEC ==================")
 #   articles1, scores1 = doc2VecFacade.get_related_articles_and_score_url(random_article_url )
 #   for idx, scr in zip(articles1[:100], scores1[:200] ):
 #       print(articleLoader.articlesDF.iloc[idx]['title'], scr)
    print(" ============= TFIDF==================")

    articles2, scores2 = tfidfFacade.get_related_articles_and_score_url(random_article_url  )
    for idx, scr in  zip(articles2[:100], scores2[:200] ):
        print(articleLoader.articlesDF.iloc[idx]['title'], scr)


