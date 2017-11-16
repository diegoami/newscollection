

import yaml
import pandas as pd

from technews_nlp_aggregator.application import Application

def direct_confront(_):
    _ = application

    user_paired = _.similarArticlesRepo.retrieve_user_paired()

    scores = retrieves_scores(_, user_paired)
    df = pd.DataFrame(scores)
    print(df.head())
    df.to_csv('data/scores.csv')


def retrieves_scores(_, user_paired):
    score_list = []
    for row in user_paired:

        article_id1, article_id2, similarity = row['SSU_AIN_ID_1'], row['SSU_AIN_ID_2'], row['SSU_SIMILARITY']
        id1, id2 = _.articleLoader.get_id_from_article_id(article_id1), _.articleLoader.get_id_from_article_id(
            article_id2)
        article1, article2 = _.articleLoader.articlesDF.iloc[id1], _.articleLoader.articlesDF.iloc[id2]

        summary1, summary2 = _.summaryFacade.full_text_summarize(id1, article1['text']), _.summaryFacade.full_text_summarize(id2, article2[
            'text'])

        score = {}
        score["SCO_T_TEXT"], score["SCO_T_TITLE"],  score["SCO_T_SUMMARY"]= scores_from_classifiers(_.tfidfFacade, article1, article2, id1, id2,
                                                                    summary1, summary2)
        score["SCO_D_TEXT"], score["SCO_D_TITLE"], score["SCO_D_SUMMARY"] = scores_from_classifiers(_.doc2VecFacade, article1, article2,
                                                                    id1, id2, summary1, summary2)
        score["SCO_DAYS"] = abs((article2['date_p'] - article1['date_p']).days)
        score["SCO_USER"] = similarity
        score_list.append(score)
    return score_list

def scores_from_classifiers(classifier, article1, article2, id1, id2, summary1, summary2):
    score = classifier.get_score_id_id(id1, id2)
    score_tit = classifier.get_score_doc_doc(article1['title'], article2['title'])
    score_sum = classifier.get_score_doc_doc(summary1, summary2)
    return score, score_tit, score_sum


if __name__ == '__main__':
    config = yaml.safe_load(open('config.yml'))
    application = Application(config, True)
    direct_confront(application)
