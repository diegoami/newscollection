
class ArticleSimilarLoader:


    def __init__(self, articlesSimilarRepo):
        self.articlesSimilarRepo = articlesSimilarRepo

    def retrieve_groups(self):
        rows = self.articlesSimilarRepo.retrieve_user_paired()
        drows = {}
        for row in rows:
            id1, id2 = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2']
            set_id = drows.get(id1, set())
            set_id.add(id2)
            drows[id1] = set_id

        done = True
        while not done:
            done = True
            for key, set_ids in drows.items():
                to_add = set()
                for id in set_ids:
                    if id in drows:
                        to_add.union(drows[id])
                        done = False
                drows[key] = drows[key].union(to_add)

        drowlist = [set([k]).union(v) for k, v in drows.items()]
        return drowlist