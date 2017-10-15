


from nltk.tokenize import sent_tokenize, word_tokenize
MIN_FREQUENCY = 3

class Tokenizer:

    def tokenize_ddf(self, articleDF):
        documents = articleDF['text'].tolist()
        titles = articleDF['title'].tolist()
        texts = [self.tokenize_doc(title, document) for title, document in zip(titles, documents)]

        # remove words that appear only once
        from collections import defaultdict
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        texts = [[token for token in text if frequency[token] >= MIN_FREQUENCY]
                 for text in texts]

    def tokenize_doc(self, document, title):
        return [word for word in word_tokenize(title.lower())] + [word for word in word_tokenize(document.lower())]



