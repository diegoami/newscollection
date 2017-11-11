from datetime import date
from technews_nlp_aggregator.common.util import conv_to_date
from .util import extract_related_articles

def merge_sims_maps(tdf_sims_map, doc2vec_sims_map, articleLoader):
    both_sims_map = {}
    for tdf_key in tdf_sims_map:
        both_sims_map[tdf_key] = (round(tdf_sims_map.get(tdf_key, 0) * 100,3) ,  round(doc2vec_sims_map.get(tdf_key, 0) * 100,3) )
    for doc2vec_key in doc2vec_sims_map:
        both_sims_map[doc2vec_key] = (round(tdf_sims_map.get(doc2vec_key, 0) * 100,3) , round(doc2vec_sims_map.get(doc2vec_key, 0) * 100,3) )
    sims = sorted(both_sims_map.items(), key=lambda x: x[1][0]+x[1][1], reverse=True)
    related_articles = extract_related_articles(articleLoader, sims)
    return related_articles



def extract_start_end(start_s, end_s):
    start, end = None, None
    if start_s:
        start = conv_to_date(start_s)
    if end_s:
        end = conv_to_date(end_s)
    if not start:
        start = date.min
    if not end:
        end = date.max
    return end, start


def retrieve_sims_map_with_dates(classifier, text, start=date.min, end=date.max, n_articles=25, title=''):
    articlesIndeces, scores = classifier.get_related_articles_and_score_doc(doc=text, start=start, end=end, title=title)
    max_n_articles = min(len(articlesIndeces), n_articles * 10)
    sims = zip(articlesIndeces[:max_n_articles], scores[:max_n_articles])
    articleMap = {articleIndex: score for articleIndex, score in sims}
    return articleMap
