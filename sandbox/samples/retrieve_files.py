import json
import argparse
if __name__ == "__main__":

    argparser = argparse.ArgumentParser()


    argparser.add_argument('--fileName')

    args = argparser.parse_args()
    with open(args.fileName) as f:
        jsload = json.load(f)

        for post in jsload["posts"]:
            title = post["title"]
            text  = post["text"]
            print(title)
            print(text)
