import json
from os.path import basename
import argparse

from gensim import corpora, models, similarities
import logging

from gensim.corpora import MmCorpus

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def load_stuff(fileName):
    articles, titles, texts, urls = [], [], [], []
    with open(fileName) as f:
        jsload = json.load(f)
        posts = jsload
        if "posts" in jsload:
            posts = jsload["posts"]
        for post in jsload["posts"]:
            title = post["title"]
            text = post["text"]
            url = post["url"]
            articles.append(title + '\n' + text)
            titles.append(title)
            texts.append(text)
            urls.append(url)
    return titles, texts, articles, urls


if __name__ == "__main__":

    def get_vec(doc,):
        vec_bow = dictionary.doc2bow(doc.lower().split())
        vec_lsi = lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi


    def get_related_articles(doc,n):
        vec_lsi = get_vec(doc)
        sims = index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return([titles[sim[0]]+":" +urls[sim[0]]  for sim in sims[:n]])

    def do_print_related(doc):
        print(" ============ BASE ARTICLE  =======================")
        print(doc)
        print(" ============ RELATED TITLES =======================")

        related_articles = get_related_articles(doc,10)
        for article in related_articles:
            print(article)

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--fileName')


    args = argparser.parse_args()
    titles, texts, documents, urls = load_stuff(args.fileName)

    dictionary = corpora.Dictionary.load(basename(args.fileName) + '.dict')  # store the dictionary, for future reference
    corpus =  MmCorpus(basename(args.fileName) + '.mm')
    lsi = models.LsiModel.load(basename(args.fileName) + '.lsi')

    index = similarities.MatrixSimilarity.load(basename(args.fileName) + '.index')  # transform corpus to LSI space and index it

    do_print_related("TO FIX ITS TOXIC AD PROBLEM, FACEBOOK MUST BREAK ITSELF\nIT IS A sure sign that Facebook’s algorithms have run amok when they allow anyone to target ads to people with an expressed interest in burning Jews. Likewise, when Russians can sow chaos in American elections by purchasing thousands of phony Facebook ads without Facebook realizing it, the automated systems selling those ads may need some oversight.")


    do_print_related("ABOUT A WEEK ago, Stanford University researchers (posted online)[https://osf.io/zn79k/] a study on the latest dystopian AI: They'd made a machine learning algorithm that essentially works as gaydar. After training the algorithm with tens of thousands of photographs from a dating site, the algorithm could, for example, guess if a white man in a photograph was gay with 81 percent accuracy. The researchers’ motives? They wanted to protect gay people. ")

    do_print_related(
        "AI RESEARCH IS IN DESPERATE NEED OF AN ETHICAL WATCHDOG\nABOUT A WEEK ago, Stanford University researchers (posted online)[https://osf.io/zn79k/] a study on the latest dystopian AI: They'd made a machine learning algorithm that essentially works as gaydar. After training the algorithm with tens of thousands of photographs from a dating site, the algorithm could, for example, guess if a white man in a photograph was gay with 81 percent accuracy. The researchers’ motives? They wanted to protect gay people. ")

    do_print_related(
        "HEY, TURN BLUETOOTH OFF WHEN YOU'RE NOT USING IT\nYOU INTUITIVELY KNOW why you should bolt your doors when you leave the house and add some sort of authentication for your smartphone. But there are lots of digital entrances that you leave open all the time, such as Wi-Fi and your cell connection. It's a calculated risk, and the benefits generally make it worthwhile. That calculus changes with Bluetooth. Whenever you don't absolutely need it, you should go ahead and turn it off.")

    do_print_related(
        "The New iPhone X packs more new stuff into any device since the original iPhone. It’s the most complete redesign of the product ever, and even offers a glimpse at what the iPhone might become when the world no longer wants smartphones.")

"""
    vec_lsi = get_vec("Human computer interaction")
    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    for sim in sims:
        print(titles[sim[0]])

"""