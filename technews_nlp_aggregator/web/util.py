from technews_nlp_aggregator.common import extract_source, extract_date_str, extract_tags
import logging
import re, html



def extract_related_articles(articleLoader, sims):
    related_articles = []


    for id, score in sims:
        link_obj = articleLoader.articlesDF.loc[id]
        related_article = fill_article(link_obj , id, score)
        related_articles.append(related_article)

    return related_articles


def fill_article(link_obj, id, score):
    related_article = {}
    related_article["id"] = str(id)
    related_article["article_id"] = str(link_obj["article_id"])
    related_article["url"] = str(link_obj["url"])
    date_p = link_obj["date_p"]
    related_article["date_p"] = str(date_p)

    related_article["title"] = str(link_obj["title"])
    related_article["source"] = extract_source(related_article["url"])

    related_article["date"] = str(date_p.year)+'-'+str(date_p.month)+'-'+str(date_p.day)
    related_article["similarity"] = score


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

def read_int_from_form(form, id, default_value="50"):
    intv_str = form.get(id, default_value)
    intv_str = intv_str.strip()
    intv = int(intv_str) if intv_str.isdigit() else default_value
    return intv

def enclose_with_span(article, str, class_id):
    try:

        article["ATX_TEXT"] = re.sub(r'\b(%s)\b'%str, '<SPAN class="'+class_id+'">' + str+ '</SPAN>', article["ATX_TEXT"], flags=re.IGNORECASE)
    except:
        logging.warning("Could not replace "+str)


def highlight_entities(article, organizations, persons, nouns):
    #article["ATX_TEXT"] = html.escape(article["ATX_TEXT"], True)
    for organization in organizations:
        enclose_with_span(article, organization, 'organization')
    for person in persons:
        enclose_with_span(article, person, 'person')
    #for noun in nouns:
    #   enclose_with_span(article, noun, 'noun')