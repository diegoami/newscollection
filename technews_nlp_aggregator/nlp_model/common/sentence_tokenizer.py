from technews_nlp_aggregator.nlp_model.spacy import spacy_nlp
sentence_excludes = [
    'This post originally appeared',
    'Command Line delivers daily updates',
    'Above:',
    'Stay tuned with our weekly recap',
    'Latest headlines delivered',
    'Copyright',
    'Intel’s rest sites and communications are subject to our Privacy Notice and Terms of Use.',
    'The views expressed are the author',
    'This story originally appeared on',
    'You can also listen on',
    'You may unsubscribe at any time.',
    'This post is part of our',
    'You can download a high-resolution version',
    'Read the original article',
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

    'The article originally appeared at',
    'Listing image by',
    'Intel’s web sites and communications are subject to our Privacy',
    'This post originated on Ars Technica UK',
    'Advance Publications owns Condé Nast',
    'We have Verge Extras, which experiments with audio and podcasting',
    'Get this deal',
    'Read next:',
    'Read:',
    'This post is part of our contributor series',
    'Country required',
    'By checking this box',
    'SEE:',
    '(Reporting by',
    'View source version on',
    'Live tweeting: Follow @verge on Twitter',
    'Here’s where to watch:',
    'HOW TO WATCH:',
    'Starting time: ',
    'Tech Republic may get a share of revenue from the sale'
    '(via'
    'Click through to find out more'
    'Image:'
]

sentence_inside_excludes = [
    'By checking this box, you are confirming you are an adult',
    'Stay tuned with our weekly recap',
    'check out our interview with',
    'Latest headlines delivered to you daily',
    'Good Deals is a weekly roundup of the best deals on the internet',
    'Read the full story'
]



class TechArticlesSentenceTokenizer():
    def remove_useless_sentences(self, sentences):

        sentences =  [ s for s in sentences if not any([x for x in sentence_excludes if s.startswith(x)])]
        sentences =  [ s for s in sentences if not any([x for x in sentence_excludes if x in s])]

        return sentences

    def sent_tokenize(self, document):
        doc_sent = spacy_nlp(document)
        sents = doc_sent.sents
        return [sent.text for sent in sents]


    def clean_sentences(self, document):
        sentences = self.sent_tokenize(document)
        sentences = self.remove_useless_sentences(sentences)
        return sentences