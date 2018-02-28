#!/bin/bash

[ $? -eq 0 ] &&  python scrape_site.py $1
[ $? -eq 0 ] &&  python scrape_urls.py $1
[ $? -eq 0 ] &&  python token_model_wf.py $1
[ $? -eq 0 ] &&  python gram_model_wf.py $1
[ $? -eq 0 ] &&  python gram_export_wf.py $1
[ $? -eq 0 ] &&  python tfidf_dictionary_wf.py $1
[ $? -eq 0 ] &&  python tfidf_model_wf.py $1
[ $? -eq 0 ] &&  python tfidf_matrix_wf.py $1
[ $? -eq 0 ] &&  python doc2vec_model_wf.py $1
[ $? -eq 0 ] &&  python similar_articles_eff.py $1


