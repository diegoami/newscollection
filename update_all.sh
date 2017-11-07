#!/bin/bash
python scrape_site.py
[ $? -eq 0 ] &&  python token_model_wf.py
[ $? -eq 0 ] &&  python gram_model_wf.py
[ $? -eq 0 ] &&  python tfidf_model_wf.py
[ $? -eq 0 ] &&  python doc2vec_model_wf.py
[ $? -eq 0 ] &&  python similar_articles_wf.py
