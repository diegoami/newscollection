class ArticleSimilarLoader:


    def __init__(self, articlesSimilarRepo, version):
        self.articlesSimilarRepo = articlesSimilarRepo
        self.version = version

    def retrieve_groups(self, articleLoader, threshold):
        articlesDF = articleLoader.articlesDF
        rows_U = self.articlesSimilarRepo.retrieve_user_paired(self.version)
        drows = []
        for row in rows_U:
            if (row['SSU_SIMILARITY'] > 0.9):
                article_id1, article_id2 = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2']
                if not articleLoader.are_same_source(article_id1, article_id2 ):
                    drows.append({article_id1, article_id2 })

        rows_C = self.articlesSimilarRepo.retrieve_classif_paired(threshold=threshold, version=self.version)

        for row in rows_C:
            article_id1, article_id2 = row['PRED_AIN_ID_1'], row['PRED_AIN_ID_2']
            if not articleLoader.are_same_source(article_id1, article_id2):
                drows.append({article_id1, article_id2})

        return self.merge_sets(drows)

    def merge_sets(self, drows):
        index_done = len(drows)-1

        while index_done > 0:
            for index_test in range(index_done-1, -1, -1):
                if len(drows[index_test].intersection(drows[index_done])) > 0:
                    drows[index_test] = drows[index_test].union(drows[index_done] )
                    del drows[index_done]
                    break
            index_done -= 1
        return drows

