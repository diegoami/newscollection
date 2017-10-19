from technews_nlp_aggregator.common import extract_source, extract_date_str, extract_tags



def extract_related_articles(articleLoader, sims):
    related_articles = []
    for id, score in sims:
        related_article = fill_article(articleLoader, score, id)
        related_articles.append(related_article)

    return related_articles

def extract_interesting_articles(articleLoader, sims):
    related_articles = []
    for url, score, connected_urls in sims:
        related_article = fill_article(articleLoader, score, url)
        connected_articles = []
        for connected_url in connected_urls:
            if (connected_url == url):
                continue
            connected_article = fill_article(articleLoader, 0, connected_url)
            connected_articles.append(connected_article)
        related_article["connected_articles"] = connected_articles
        related_articles.append(related_article)

    return related_articles

def fill_article(articleLoader, score, id):
    related_article = {}
    link_obj = articleLoader.articlesDF.loc[id]
    related_article["id"] = str(id)
    related_article["article_id"] = str(link_obj["article_id"])
    related_article["url"] = str(link_obj["url"])
    related_article["date_p"] = str(link_obj["date_p"])

    related_article["title"] = str(link_obj["title"])
    related_article["tags"], related_article["tag_base"]  = [], []
    related_article["source"] = extract_source(related_article["url"])

    related_article["date"] = extract_date_str(related_article["url"])


    related_article["similarity"] = score * 100
    related_article["authors"], related_article["author_base"]  = [], []

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

