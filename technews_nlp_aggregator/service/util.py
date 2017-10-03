from urllib.parse import urlparse
from datetime import date


def extract_tags(tags):
    tag_base = [x.split('/')[-1] if len(x.split('/')[-1]) > 0 else x.split('/')[-2] for x in
                tags]
    return tag_base


def extract_date(url):
    arrs = str(urlparse(url)[2]).split('/')
    index = 0
    while not arrs[index].isdigit():
        index += 1
    year, month, day = arrs[index], arrs[index + 1], arrs[index + 2]
    date_str = day + '-' + month + '-' + year

    return date_str

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
    related_article["date"] = extract_date(related_article["url"])
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

def extract_source( url):
    source = str(urlparse(url)[1]).upper()
    return source


def conv_to_date(str_date):
    try:
        return date(*(map(int, str_date.split('-'))))
    except:
        return None