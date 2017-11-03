import re

class TechArticlesCleaner():
    monthExpr = 'January|February|March|April|May|June|July|August|September|October|November|December'
    twitterLongUrl = re.compile(r'(pic\.twitter\.com\/[a-zA-Z0-9]{10}\s*?\—.*?\(\@[a-zA-Z0-9_]+\)\s+)(%s)(\s[0-9]{1,2},\s20[0-9]{1,2})' % monthExpr,re.VERBOSE)

    twitterSecondPart = re.compile(r'(\—.*?\(\@[a-zA-Z0-9_]+\)\s+)(%s)(\s[0-9]{1,2},\s20[0-9]{1,2})' % monthExpr,re.VERBOSE)

    twitterHashtag = re.compile(r'\#[A-Za-z0-9]+pic\.twitter\.com\/[a-zA-Z0-9]{10}')
    twitterShort = re.compile(r'pic\.twitter\.com\/[a-zA-Z0-9]{10}')
    tcoShort = re.compile(r'https\:\/\/t\.co\/[a-zA-Z0-9]{10}')

    def remove_chars(self, doc):
        doc = doc.replace('“', '').replace('”', '')
        return doc

    def replace_tweets(self, doc):
        doc = self.twitterLongUrl.sub('', doc)
        doc = self.twitterSecondPart.sub('', doc)
        doc = self.twitterHashtag.sub('', doc)
        doc = self.twitterShort .sub('', doc)
        doc = self.tcoShort.sub('', doc)

        return doc

    def do_clean(self, doc):
        doc = self.remove_chars(doc)

        doc = self.replace_tweets(doc)
        return doc

