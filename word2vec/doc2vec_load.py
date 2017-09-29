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

model_filename = '/media/diego/QData/techarticles/models/doc2vecmodel_2017-09-29T18:06:10.658360.model'
logging.info("Training completed, saving to  " + model_filename)
model = Doc2Vec.load(model_filename)
#for docvec in model.docvecs:
#    print(docvec)
while True:
    s = input('--> ')
    #print(model.docvecs.most_similar(st, topn=200))
    st = s.split()
    infer_vector = model.infer_vector(st)

    similar_documents = model.docvecs.most_similar([infer_vector], topn=10)
    print(similar_documents)