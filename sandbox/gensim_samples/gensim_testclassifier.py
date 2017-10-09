import argparse
import logging
import sys
from os.path import basename

sys.path.append('..')
from sandbox.gensim_samples import GensimClassifier

logging.basicConfig(filename='logs/info.log',level=logging.INFO)



if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--fileName')
    args = argparser.parse_args()
    base = basename(args.fileName)
    gensimClassifier = GensimClassifier(article_filename=args.fileName,  dict_filename=args.fileName + '.dict',
                corpus_filename=args.fileName + '.mm', lsi_filename=args.fileName + '.lsi', index_filename=args.fileName + '.index')
    gensimClassifier.load_articles()
    gensimClassifier.load_models()

    gensimClassifier.do_print_related("TO FIX ITS TOXIC AD PROBLEM, FACEBOOK MUST BREAK ITSELF\nIT IS A sure sign that Facebook’s algorithms have run amok when they allow anyone to target ads to people with an expressed interest in burning Jews. Likewise, when Russians can sow chaos in American elections by purchasing thousands of phony Facebook ads without Facebook realizing it, the automated systems selling those ads may need some oversight.")

    gensimClassifier.do_print_related("ABOUT A WEEK ago, Stanford University researchers (posted online)[https://osf.io/zn79k/] a study on the latest dystopian AI: They'd made a machine learning algorithm that essentially works as gaydar. After training the algorithm with tens of thousands of photographs from a dating site, the algorithm could, for example, guess if a white man in a photograph was gay with 81 percent accuracy. The researchers’ motives? They wanted to protect gay people. ")

    gensimClassifier.do_print_related(
        "AI RESEARCH IS IN DESPERATE NEED OF AN ETHICAL WATCHDOG\nABOUT A WEEK ago, Stanford University researchers (posted online)[https://osf.io/zn79k/] a study on the latest dystopian AI: They'd made a machine learning algorithm that essentially works as gaydar. After training the algorithm with tens of thousands of photographs from a dating site, the algorithm could, for example, guess if a white man in a photograph was gay with 81 percent accuracy. The researchers’ motives? They wanted to protect gay people. ")

    gensimClassifier.do_print_related(
        "HEY, TURN BLUETOOTH OFF WHEN YOU'RE NOT USING IT\nYOU INTUITIVELY KNOW why you should bolt your doors when you leave the house and add some sort of authentication for your smartphone. But there are lots of digital entrances that you leave open all the time, such as Wi-Fi and your cell connection. It's a calculated risk, and the benefits generally make it worthwhile. That calculus changes with Bluetooth. Whenever you don't absolutely need it, you should go ahead and turn it off.")

    gensimClassifier.do_print_related(
        "The New iPhone X packs more new stuff into any device since the original iPhone. It’s the most complete redesign of the product ever, and even offers a glimpse at what the iPhone might become when the world no longer wants smartphones.")
