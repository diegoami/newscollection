from technews_nlp_aggregator.common import extract_source, extract_date_str, extract_tags



def extract_related_articles(articleLoader, sims):
    related_articles = []
    for url, score in sims:
        related_article = fill_article(articleLoader, score, url)
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

def fill_article(articleLoader, score, url):
    related_article = {}
    related_article["url"] = url
    link_obj = articleLoader.article_map[url]
    related_article["title"] = link_obj["title"]
    related_article["tags"] = link_obj["tags"]
    related_article["source"] = extract_source(url)
    related_article["tag_base"] = extract_tags(related_article["tags"])
    related_article["date"] = extract_date_str(related_article["url"])
    related_article["similarity"] = score * 100
    related_article["authors"] = link_obj["authors"]
    related_article["author_base"] = extract_tags(related_article["authors"])
    return related_article


def filter_double(articleLoader, sims):
    related_articles = []
    found_articles = []
    for url, score, connected_urls in sims:
        if url in found_articles:
            continue
        else:
            related_articles.append((url,score, connected_urls))
            found_articles.extend(connected_urls)
    return related_articles

