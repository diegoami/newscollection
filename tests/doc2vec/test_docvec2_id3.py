import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from technews_nlp_aggregator.nlp_model.publish import TfidfFacade, Doc2VecFacade
import yaml
from gensim.models import Doc2Vec


from technews_nlp_aggregator.nlp_model.common import ArticleLoader
from technews_nlp_aggregator.persistence.article_dataset_repo import ArticleDatasetRepo
import yaml

config = yaml.safe_load(open('../../config.yml'))
db_config = yaml.safe_load(open(config["db_key_file"]))

articleDatasetRepo = ArticleDatasetRepo(db_config["db_url"])
articleLoader = ArticleLoader(articleDatasetRepo)
articleLoader.load_all_articles(False)

doc2VecFacade = Doc2VecFacade(config["doc2vec_models_file_link"], articleLoader)
doc2VecFacade.load_models()
model = doc2VecFacade.model
while True:
    st = input('--> ').lower()
    pos, neg = st.split(',')
    posl, negl = pos.split(), neg.split()
    print(posl, negl)
    print(model.most_similar(positive=posl, negative=negl))