from technews_nlp_aggregator.common import extract_source, extract_date_str, extract_tags
import logging
import re, html


def extract_related_articles(articleLoader, scoresDF, ssusDF=None, sscsDF=None):

    def score_row(row):
        row["similarity"] = (row['score_t'], row['score_d'])
        return row

    merged_DF =  scoresDF.join(articleLoader.articlesDF)
    if (ssusDF is not None):
        merged_DF =  merged_DF.merge(ssusDF, on='article_id', how='left')
    if (sscsDF is not None):
        merged_DF =  merged_DF.merge(sscsDF, on='article_id', how='left')
    merged_DF = merged_DF.apply(score_row,axis=1)
    merged_DF['date'] = merged_DF['date_p'].map(lambda date_p: str(date_p.year)+'-'+str(date_p.month)+'-'+str(date_p.day))
    related_articles = merged_DF.to_dict(orient='records')
    return related_articles



def read_int_from_form(form, id, default_value="50"):
    intv_str = form.get(id, default_value)
    if (intv_str):
        intv_str = intv_str.strip()
    else:
        intv_str = default_value
    if intv_str:
        intv = int(intv_str) if intv_str.isdigit() else default_value
        return intv
    else:
        return None

def enclose_with_span(article, str, class_id):
    try:
        article["ATX_TEXT"] = re.sub(r'\b(%s)\b'%str, '<SPAN class="'+class_id+'">' + str+ '</SPAN>', article["ATX_TEXT"], flags=re.IGNORECASE)
    except:
        logging.warning("Could not replace "+str)
