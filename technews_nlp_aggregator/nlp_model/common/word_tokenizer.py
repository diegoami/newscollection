import logging
from string import punctuation
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from technews_nlp_aggregator.nlp_model.spacy import spacy_nlp

class TechArticlesWordTokenizer:



    def tokenize_sentences(self, all_sentences):
        tokenized_sentences = []
        for sentence in all_sentences:
            tokenized_sentences.append(self.tokenize_sentence(sentence))
        return tokenized_sentences

    def tokenize_sentence(self, sentence):
        tok_doc = spacy_nlp(sentence.lower())
        return [word.text for word in tok_doc]