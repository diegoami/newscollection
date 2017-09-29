from os import listdir
from os.path import isfile, join
from gensim.models.doc2vec import TaggedDocument
from datetime import datetime
import json
from gensim.models import Doc2Vec
import os
import logging

import sys
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

root_dir = '/media/diego/QData/techarticles/'
corpus_dir = root_dir+'parsed_articles/'
listname = root_dir +'lists/article_list_29_09_2017b.json'


docLabels = []
data = []
with open(listname, 'r') as lst_f:
    article_map = json.load(lst_f)
    for url in sorted(article_map):
        record = article_map[url]
        filename = corpus_dir+ '/' + record["filename"]
        if (os.path.isfile(filename)):

            with open(filename, 'r') as f:
                text = f.read()
                if (len(text) > 400):
                    data.append(text)
                    docLabels.append(url)

#docLabels = [f for f in listdir(corpus_dir) if f.endswith('.txt')]


#for doc in docLabels:
#    data.append(open(corpus_dir + doc, 'r'))

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
       self.labels_list = labels_list
       self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            #yield LabeledSentence(words=doc.split(),labels=[self.labels_list[idx]])
            #stop = stopwords.words('english') + list(string.punctuation)
            wtok = [i for i in word_tokenize(doc)]
            tags = [self.labels_list[idx]]

            #for s in stok:
             #   wtok = [i for i in word_tokenize(s)]
                #print("Now processing....")
                #print(wtok)
            yield TaggedDocument(words=wtok, tags=tags)

it = LabeledLineSentence(data, docLabels)

model = Doc2Vec(size=300, window=10, min_count=5, workers=11,alpha=0.025, min_alpha=0.025, iter=10) # use fixed learning rate
model.build_vocab(it)

logging.info("Starting to train......")

#for epoch in range(10):
#    logging.info("On epoch "+str(epoch))
    #model.train(it)
#model.alpha -= 0.002 # decrease the learning rate
#model.min_alpha = model.alpha # fix the learning rate, no deca
model.train(it,  total_examples=model.corpus_count, epochs=model.iter)
 #   logging.info("Finished training epoch " + str(epoch))
model_filename = root_dir + 'models/doc2vec/doc2vecmodel_'+ datetime.now().isoformat()+'.model'

logging.info("Training completed, saving to  " + model_filename)
model.save(model_filename)