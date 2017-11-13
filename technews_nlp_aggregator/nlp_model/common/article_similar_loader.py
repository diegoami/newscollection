
class ArticleSimilarLoader:


    def __init__(self, articlesSimilarRepo):
        self.articlesSimilarRepo = articlesSimilarRepo

    def retrieve_groups(self):
        rows = self.articlesSimilarRepo.retrieve_user_paired()
        drows = {}
        for row in rows:
            if (row['SSU_SIMILARITY'] > 0.9):
                id1, id2 = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2']
                set_id = drows.get(id1, set())
                set_id.add(id2)
                drows[id1] = set_id

        return self.merge_sets(drows)

    def merge_sets(self, drows):
        done = False
        while not done:
            done = True
            for key, set_ids in drows.items():
                to_add = set()
                if (len(set_ids) > 0):
                    for id in set_ids:
                        if id in drows and len(drows[id]) > 0:
                            to_add = to_add.union(drows[id])
                            drows[id] = {}
                            done = False
                    if (len(to_add)):
                        drows[key] = drows[key].union(to_add)


        drowlist = [{k}.union(v) for k, v in drows.items() if len(v) > 0]
        return drowlist



if __name__ == '__main__':
    dks = [
        {1 : {2}, 2: {3}},

        {1: {4, 7}, 2: {3}, 5 : {8}, 4 : {9} , 2: {5,10}, 11: {12} , 6: {12,13}}

    ]
    articleSimilarLoader = ArticleSimilarLoader(None)
    for dk in dks:
        print(articleSimilarLoader.merge_sets(dk))