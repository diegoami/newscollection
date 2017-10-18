from nltk.tokenize import sent_tokenize
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentence_excludes = [
    'This post originally appeared',
    'Command Line delivers daily updates',
    'Above:',
    'Stay tuned with our weekly recap',
    'Latest headlines delivered',
    'Copyright',
    'Intel’s web sites and communications are subject to our Privacy Notice and Terms of Use.',
    'The views expressed are the author\'s own',
    'This story originally appeared on',
    'You can also listen on',
    'You may unsubscribe at any time.',
    'This post is part of our',
    'You can download a high-resolution version',
    'Read the original article',
    'Country required',
    'It is written and published independently',
    'For more information',
    'This article was originally published',
    'ProBeat is a column in which Emil rants',
    'You can find them all in iTunes',
    'For more CES 2017 news from TNW',
    'This article is part of our',
    'This isn’t a sponsored post',
    'Our coverage remains objective',
    'This poll is closed',
    'This article is part of our',
    'via TechCrunch',
    'Check out our merch store here',
    'Let us know in the comments',
    'If you’re interested in learning more',
    'Via Engadget',
    'You can read the',
    'Follow all our coverage',
    'Photography by',
    'Sign up for their newsletter',
    'Via Android Police',
    'via Mashable',
    'If you purchase them through our links',
    'via Mashable',
    'These do not influence editorial content',
    'Vox Media has affiliate partnerships',
    'You might also want to check out',
    'Sponsors make TechCrunch',
    '(Disclosure:',
    'Either way, if you buy something through our affiliate link',
    'We sometimes update and/or re-publish articles from our archives',
    'If you are interested in learning more about sponsorship opportunities',
    'See you soon',
    'Disclosure:',
    'If you are interested in learning more about sponsorships',
    'Enjoy, and have a great weekend!',
    'You can submit deals to deals@theverge.com',
    'Our sponsors help make Disrupt happen',
    'This post was originally published by',
    'This post is not sponsored, but',
    'This post was originally published by',
    'Thanks!',
    'The article originally appeared at'

]



sentence_inside_excludes = [
    'By checking this box, you are confirming you are an adult',
    'Stay tuned with our weekly recap',
    'check out our interview with',
    'Latest headlines delivered to you daily'

]


class SimpleSentenceTokenizer:
    def process(self, title, document):
        sentences = sent_tokenize(document)
        return sentences

class TechArticlesSentenceTokenizer(SimpleSentenceTokenizer):
    def remove_useless_sentences(self, sentences):

        sentences =  [ s for s in sentences if not any([x for x in sentence_excludes if s.startswith(x)])]
        sentences =  [ s for s in sentences if not any([x for x in sentence_excludes if x in s])]

        return sentences

    def process(self, title, document):

        sentences = sent_tokenize(document)
        real_sentences = self.remove_useless_sentences(sentences)

        if (sentences[0].startswith(title)):
            return real_sentences
        else:
            return [title + "." ]+ real_sentences