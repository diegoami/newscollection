import spacy

spacy_nlp = spacy.load('en')
# print(random_article)

def sanitize_ent(ents, all_ents):
    result = set()
    for ent in ents:
        if ent.lower() not in(["span", "class", "person", "noun", "organization"]):
            if not any([x for x in all_ents if len(x) > len(ent) and ent.lower() in x.lower()]):
                result.add(ent)

    return result

def retrieve_entities(article_text):
    organizations, persons, nouns = set(), set(), set()
    doc = spacy_nlp (article_text)
    for ent in doc.ents:
        if (ent.label_ == 'ORG'):
            organizations.add(ent.text)
        if (ent.label_ == 'PERSON'):
            persons.add(ent.text)
    for token in doc:
        if ((token.pos_ == 'NOUN' or token.pos_ == 'NNP') and token.text.istitle()):
            nouns.add(token.text)
    allents = set().union(organizations).union(persons)
    organizations, persons, nouns = \
        sanitize_ent(organizations, organizations), \
        sanitize_ent(persons, organizations.union(persons)), \
        sanitize_ent(nouns, organizations.union(persons).union(nouns))
    return organizations, persons, nouns


def retrieve_sp_words(article_text):
    doc = spacy_nlp (article_text)
    return doc
