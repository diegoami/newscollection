from random import randint
from flask import  request, render_template
from technews_nlp_aggregator.nlp_model.spacy.entities import retrieve_entities
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from . import app
import re

@app.route('/duplicates/<int:page_id>')
def duplicates(page_id=0):
    all_articles = app.application.similarArticlesRepo.list_similar_articles()
    start, end = page_id*100, (page_id+1)*100
    if (len(all_articles) > start):
        has_next = len(all_articles) > end
        dup_articles = all_articles[start:min(end,len(all_articles))]
    else:
        dup_articles = []
    return render_template('duplicates.html', dup_articles=dup_articles, page_id=page_id, has_next=has_next)


def enclose_with_span(article, str, class_id):
    try:
        article["ATX_TEXT"] = re.sub(str, '<SPAN class="'+class_id+'">' + str+ '</SPAN>', article["ATX_TEXT"])
    except:
        logging.warning("Could not replace "+str)


@app.route('/compare/<int:id1>/<int:id2>')
def compare(id1, id2):
    article1, article2 = app.application.articleDatasetRepo.load_articles_with_text(id1, id2)
    article1["TAGS"], article1["AUTHORS"] = app.application.articleDatasetRepo.retrieve_tags_authors(id1)
    article2["TAGS"], article2["AUTHORS"] = app.application.articleDatasetRepo.retrieve_tags_authors(id2)
    article1["ORGANIZATIONS"], article1["PERSONS"] = retrieve_entities(article1["ATX_TEXT"])
    article2["ORGANIZATIONS"], article2["PERSONS"] = retrieve_entities(article2["ATX_TEXT"])

    for organization in article1["ORGANIZATIONS"]:
        enclose_with_span(article1, organization, 'organization')
    for organization in article2["ORGANIZATIONS"]:
        enclose_with_span(article2, organization, 'organization')

    return render_template('to_compare.html', A1=article1, A2=article2)



@app.route('/randomrelated')
def randomrelated():
    all_similar_articles = app.application.similarArticlesRepo.list_similar_articles()
    len_similar_articles= len(all_similar_articles )
    rlena = randint(0,len_similar_articles)
    similar_article_pair = all_similar_articles[rlena]
    id1, id2 = similar_article_pair["ID_1"], similar_article_pair["ID_2"]

    return compare(id1, id2)

def save_user_association(id1,id2, similarity):
    app.application.similarArticlesRepo.persist_user_association(id1, id2, similarity, request.environ['REMOTE_ADDR'])
    return randomrelated()

@app.route('/samestory/<int:id1>/<int:id2>')
def samestory(id1, id2):
    return save_user_association(id1,id2, 1)

@app.route('/related/<int:id1>/<int:id2>')
def related(id1, id2):
    return save_user_association(id1, id2, 0.5)

@app.route('/unrelated/<int:id1>/<int:id2>')
def unrelated(id1, id2):
    return save_user_association(id1, id2, 0)



