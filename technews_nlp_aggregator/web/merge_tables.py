from datetime import date
from technews_nlp_aggregator.common.util import conv_to_date
from .util import extract_related_articles
import numpy as np
import pandas as pd

def merge_sims_maps(tdf_DF, doc2vec_DF, articleLoader, n_articles=100, page_id = 0):
    new_DF = tdf_DF.join(doc2vec_DF, lsuffix='_t', rsuffix='_d')
    new_DF['score_sums'] = new_DF['score_t'] + new_DF['score_d']
    new_DF.sort_values(by='score_sums', inplace=True, ascending=False)
    start, end = page_id * n_articles, (page_id + 1) * n_articles
    if (len(new_DF) > start):
        has_next = len(new_DF) > end
        new_DF = new_DF.iloc[start:min(end, len(new_DF))]
        related_articles = extract_related_articles(articleLoader, new_DF )
        return related_articles
    else:
        return None




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
    scoresDF = classifier.get_related_articles_and_score_doc(doc=text, start=start, end=end, title=title)

    return scoresDF
