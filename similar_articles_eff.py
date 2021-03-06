
import traceback
import logging
import sys
from technews_nlp_aggregator.common import load_config
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from technews_nlp_aggregator import Application


def process_for_insertion(id, df, threshold, articleFilterDF):

    for other_id, row in df.iterrows():
        score = row['score']
        if score >= threshold and score < 0.995:
            article_id, article_other_id = articleFilterDF.iloc[id]['article_id'], articleFilterDF.iloc[other_id]['article_id']
            logging.info("Yielding {}, {}, {}".format(article_id, article_other_id, score))
            yield (article_id, article_other_id, score)



def eff_similar_articles(application, tf_threshold=0.58, doc_threshold = 0.3, d_days=2):
    logging.info("Searching articles : {} tf, {} doc, {} d_days".format(tf_threshold, doc_threshold, d_days))
    _ = application
    articlesToProcessDF =  _.articleLoader.articlesDF[_.articleLoader.articlesDF['processed'].isnull()]
    con = _.similarArticlesRepo.get_connection()
    logging.info("{} articles to process".format(len(articlesToProcessDF)))

    for id, row in articlesToProcessDF.iterrows():
        article_id = row['article_id']
        article_date = row['date_p']
        logging.info("Processing article : {}".format(article_id))

        tfidf_DF= _.tfidfFacade.get_related_articles_for_id(id, d_days)
        doc2vec_DF = _.doc2VecFacade.get_related_articles_for_id(id,  d_days)
        logging.info("Found {} tf, {} doc".format(len(tfidf_DF), len(doc2vec_DF)))
        try:
            con.begin()
            logging.info("Processing similar TFs...")
            for article1, article2, score in process_for_insertion(id, tfidf_DF, tf_threshold, _.articleLoader.articlesDF):
                _.similarArticlesRepo.persist_association(con, article1, article2,  _.tfidfFacade.name, score)
            logging.info("Processing similar Doc2Vecs...")
            for article1, article2, score in process_for_insertion(id, doc2vec_DF, doc_threshold,  _.articleLoader.articlesDF ):
                _.similarArticlesRepo.persist_association(con, article1, article2, _.doc2VecFacade.name, score)

            _.similarArticlesRepo.update_to_processed(article_id, con)
            con.commit()
        except:
            traceback.print_exc()
            con.rollback()




if __name__ == '__main__':
    config = load_config(sys.argv)
    application = Application(config, True)
    eff_similar_articles(application, float(config['tf_threshold']), float(config['doc_threshold']), float(config.get('d_days',2) ))

