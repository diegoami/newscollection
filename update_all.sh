#!/bin/bash

find /media/diego/QData/techarticles/models/doc2vec   -type d | xargs rm -f -r
find /media/diego/QData/techarticles/models/lsi -type d | xargs rm -f -r
find /media/diego/QData/techarticles/models/phrases -type d | xargs rm -f -r
find /media/diego/QData/techarticles/pickle -mtime +2 -type d | xargs rm -f -r

source activate tnaggregator-2
[ $? -eq 0 ] &&  python scrape_site.py
[ $? -eq 0 ] &&  python token_model_wf.py --action append
[ $? -eq 0 ] &&  python gram_model_wf.py
[ $? -eq 0 ] &&  python gram_export_wf.py
[ $? -eq 0 ] &&  python tfidf_dictionary_wf.py
[ $? -eq 0 ] &&  python tfidf_model_wf.py
[ $? -eq 0 ] &&  python tfidf_matrix_wf.py
[ $? -eq 0 ] &&  python doc2vec_model_wf.py
[ $? -eq 0 ] &&  python similar_articles_wf.py
