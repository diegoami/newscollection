import spacy

nlp = spacy.load('en')

# print(random_article)


def retrieve_entities(article_text):
    organizations, persons = set(), set()
    doc = nlp(article_text)
    for ent in doc.ents:
        if (ent.label_ == 'ORG'):
            organizations.add(ent.text)
        if (ent.label_ == 'PERSON'):
            persons.add(ent.text)

    return organizations, persons
