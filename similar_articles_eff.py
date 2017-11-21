

import yaml
import traceback
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

from technews_nlp_aggregator import Application


def process_for_insertion(id, df, threshold, articleFilterDF):

    for other_id, row in df.iterrows():
        score = row['score']
        if score >= threshold and score < 0.995:
            article_id, article_other_id = articleFilterDF.iloc[id]['article_id'], articleFilterDF.iloc[other_id]['article_id']
            logging.debug("Yielding {}, {}, {}".format(article_id, article_other_id, score))
            yield (article_id, article_other_id, score)



def eff_similar_articles(application):
    _ = application
    articleFilterDF = _.articleLoader.articlesDF[:_.tfidfFacade.docs_in_model()]
    articlesToProcessDF =  articleFilterDF [_.articleLoader.articlesDF['processed'].isnull()]
    con = _.similarArticlesRepo.get_connection()
    for id, row in articlesToProcessDF.iterrows():
        article_id = row['article_id']
        article_date = row['date_p']
        logging.debug("Processing article : {}".format(article_id))

        tfidf_DF= _.tfidfFacade.get_related_articles_for_id(id, 2)
        doc2vec_DF = _.doc2VecFacade.get_related_articles_for_id(id,  2)

        try:
            con.begin()
            for article1, article2, score in process_for_insertion(id, tfidf_DF, 0.56, articleFilterDF):
                _.similarArticlesRepo.persist_association(con, article1, article2,  _.tfidfFacade.name, score)

            for article1, article2, score in process_for_insertion(id, doc2vec_DF, 0.28,  articleFilterDF):
                _.similarArticlesRepo.persist_association(con, article1, article2, _.doc2VecFacade.name, score)

            _.similarArticlesRepo.update_to_processed(article_id, con)
            con.commit()
        except:
            traceback.print_exc()
            con.rollback()




if __name__ == '__main__':

    config = yaml.safe_load(open('config.yml'))
    application = Application(config, True)
    eff_similar_articles(application)
