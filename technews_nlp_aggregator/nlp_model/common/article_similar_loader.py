import logging

class ArticleSimilarLoader:


    def __init__(self, articlesSimilarRepo, version, threshold=0.9):
        self.articlesSimilarRepo = articlesSimilarRepo
        self.version = version
        self.threshold = threshold

    def retrieve_groups(self, articleLoader, threshold):
        logging.info("ArticleSimilarLoader: Retrieving groups....")
        articlesDF = articleLoader.articlesDF
        logging.info("Retrieving user paired...")
        rows_U = self.articlesSimilarRepo.retrieve_user_paired(self.version)
        logging.info("Finished retrieving {} user paired...".format(len(rows_U)))
        drows = []
        for row in rows_U:
            if (row['SSU_SIMILARITY'] > self.threshold):
                article_id1, article_id2 = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2']
                if not articleLoader.are_same_source(article_id1, article_id2 ):
                    drows.append({article_id1, article_id2 })

        logging.info("Finished processing user paired...".format(len(rows_U)))

        logging.info("Retrieving classif_paired...")
        rows_C = self.articlesSimilarRepo.retrieve_classif_paired(threshold=threshold, version=self.version)
        logging.info("Retrieved {} classif_ paired...".format(len(rows_C )))

        for row in rows_C:
            article_id1, article_id2 = row['PRED_AIN_ID_1'], row['PRED_AIN_ID_2']
            if not articleLoader.are_same_source(article_id1, article_id2):
                drows.append({article_id1, article_id2})

        logging.info("Finished processing classif paired...".format(len(rows_U)))

        return self.merge_sets(drows)

    def merge_sets(self, drows):
        logging.info("Articlesimilarloader-mergeset: {} to process ".format(len(drows)))
        index_done = len(drows)-1

        while index_done > 0:
            for index_test in range(index_done-1, -1, -1):
                if len(drows[index_test].intersection(drows[index_done])) > 0:
                    drows[index_test] = drows[index_test].union(drows[index_done] )
                    del drows[index_done]
                    break
            index_done -= 1
            if (index_done % 2000 == 0):
                logging.info("Still {} merge sets to process".format(index_done))
        return drows

