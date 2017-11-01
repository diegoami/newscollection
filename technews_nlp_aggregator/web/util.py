from technews_nlp_aggregator.common import extract_source, extract_date_str, extract_tags



def extract_related_articles(articleLoader, sims):
    related_articles = []


    for id, score in sims:
        link_obj = articleLoader.articlesDF.loc[id]
        tags, authors  = articleLoader.retrieve_meta(id)
        related_article = fill_article(link_obj , id, score, tags, authors  )
        related_articles.append(related_article)

    return related_articles


def fill_article(link_obj, id, score, tags, authors):
    related_article = {}
    related_article["id"] = str(id)
    related_article["article_id"] = str(link_obj["article_id"])
    related_article["url"] = str(link_obj["url"])
    date_p = link_obj["date_p"]
    related_article["date_p"] = str(date_p)

    related_article["title"] = str(link_obj["title"])
    related_article["source"] = extract_source(related_article["url"])

    related_article["date"] = str(date_p.year)+'-'+str(date_p.month)+'-'+str(date_p.day)
    related_article["similarity"] = round(score * 100,3)
    related_article["tags"] = tags
    related_article["authors"] = authors

    return related_article


def filter_double(articleLoader, sims):
    related_articles = []
    found_articles = []
    for id, score, connected_ids in sims:
        if id in found_articles:
            continue
        else:
            related_articles.append((id,score, connected_ids))
            found_articles.extend(connected_ids)
    return related_articles

def read_int_from_form(form, id):
    intv_str = form.get(id, '50')
    intv = int(intv_str) if intv_str.isdigit() else 50
    return intv
