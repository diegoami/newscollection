from gensim_samples.gensim_loader import GensimLoader
from gensim.models import word2vec
import logging
import sys
sys.path.append('/home/diegoami/PycharmProjects/Newscollection')
from gensim.models.word2vec import Word2Vec
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from datetime import datetime

gensimLoader = GensimLoader()
print('Loading articles'.format(len(gensimLoader.articles)))
gensimLoader.load_articles_from_directory(dirname='/home/diego/qdata/techarticles/parsed_articles/')
import spacy
nlp = spacy.load('en')                 # You are here.

sentences = []
print('{} articles loaded'.format(len(gensimLoader.articles)))

from gensim.parsing import PorterStemmer

global_stemmer = PorterStemmer()


class StemmingHelper(object):
    """
    Class to aid the stemming process - from word to stemmed form,
    and vice versa.
    The 'original' form of a stemmed word will be returned as the
    form in which its been used the most number of times in the text.
    """

    # This reverse lookup will remember the original forms of the stemmed
    # words
    word_lookup = {}

    @classmethod
    def stem(cls, word):
        """
        Stems a word and updates the reverse lookup.
        """

        # Stem the word
        stemmed = global_stemmer.stem(word)

        # Update the word lookup
        if stemmed not in cls.word_lookup:
            cls.word_lookup[stemmed] = {}
        cls.word_lookup[stemmed][word] = (
            cls.word_lookup[stemmed].get(word, 0) + 1)

        return stemmed

    @classmethod
    def original_form(cls, word):
        """
        Returns original form of a word given the stemmed version,
        as stored in the word lookup.
        """

        if word in cls.word_lookup:
            return max(cls.word_lookup[word].keys(),
                       key=lambda x: cls.word_lookup[word][x])
        else:
            return word

for index, article in enumerate(gensimLoader.articles):
    if (index % 1000):
        print('Processed {} articles'.format(index))
    doc = nlp.make_doc(article )
    sentences_article = [sent.string.strip() for sent in doc.sents]
    sentences = sentences + sentences_article

print('Creating word2vec model....')

model = Word2Vec(sentences)
model_filename = '/home/diego/qdata/models/word2vec/word2vec_model_'+ datetime.now().isoformat()+'.model'
model.save(model_filename)