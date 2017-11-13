
class ArticleSimilarLoader:


    def __init__(self, articlesSimilarRepo):
        self.articlesSimilarRepo = articlesSimilarRepo

    def retrieve_groups(self):
        rows = self.articlesSimilarRepo.retrieve_user_paired()
        drows = []
        for row in rows:
            if (row['SSU_SIMILARITY'] > 0.9):
                id1, id2 = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2']
                drows.append({id1,id2})

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

if __name__ == '__main__':
    dks = [
        [{1,3}, {2, 3}],

        [{1,2}, {2, 3}],
        [{1, 4, 7}, {2, 3, 5},  {4 , 8}, {2, 9} , {2, 5,10}, {11, 12} , {6,12,13}]

    ]
    articleSimilarLoader = ArticleSimilarLoader(None)
    for dk in dks:
        print(articleSimilarLoader.merge_sets(dk))