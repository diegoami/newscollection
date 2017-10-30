
from nltk.tokenize import sent_tokenize, word_tokenize

chars_to_remove = ['“', '”']
import re

def remove_chars(str):

    str = str.replace("“", "").replace("”","")
    return str

class NltkWordTokenizer:



    def tokenize_sentence(self, all_sentences):
        tokenized_sentences = []
        for sentence in all_sentences:
            tokenized_sentences.append([remove_chars(word) for word in word_tokenize(sentence.lower())])
        return tokenized_sentences