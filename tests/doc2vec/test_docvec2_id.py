import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from technews_nlp_aggregator.nlp_model.publish import TfidfFacade, Doc2VecFacade
import yaml
from gensim.models import Doc2Vec


from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
import yaml

config = yaml.safe_load(open('../../config.yml'))
db_config = yaml.safe_load(open(config["key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(False)

doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader)
doc2VecFacade.load_models()
model = doc2VecFacade.model
while True:
    st = input('--> ').lower()
    if st in model.wv.vocab:
      #  print(model.score(st))
        print(model.most_similar(st))

    for s in st.split():
        if s in model.wv.vocab:
            print(model.most_similar(s))
