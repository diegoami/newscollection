#!/bin/bash

#[ $? -eq 0 ] &&  python gram_model_wf.py
#[ $? -eq 0 ] &&  python gram_export_wf.py
#[ $? -eq 0 ] &&  python tfidf_dictionary_wf.py
#[ $? -eq 0 ] &&  python tfidf_model_wf.py
#[ $? -eq 0 ] &&  python tfidf_matrix_wf.py
[ $? -eq 0 ] &&  python doc2vec_model_wf.py
[ $? -eq 0 ] &&  python create_train_data.py
[ $? -eq 0 ] &&  python do_boost.py


