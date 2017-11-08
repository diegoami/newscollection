#!/bin/bash
python scrape_site.py
[ $? -eq 0 ] &&  python token_model_wf.py --action update
[ $? -eq 0 ] &&  python gram_model_wf.py
[ $? -eq 0 ] &&  python gram_export_wf.py
[ $? -eq 0 ] &&  python tfidf_dictionary_wf.py
[ $? -eq 0 ] &&  python tfidf_model_wf.py
[ $? -eq 0 ] &&  python tfidf_matrix_wf.py
[ $? -eq 0 ] &&  python doc2vec_model_wf.py
[ $? -eq 0 ] &&  python similar_articles_wf.py
wrong command
if [ $? -eq 0 ] ; then
     find /media/diego/QData/techarticles/models/doc2vec | xargs rm -f -r
     find /media/diego/QData/techarticles/models/lsi | xargs rm -f -r
     find /media/diego/QData/techarticles/models/phrases | xargs rm -f -r
     find /media/diego/QData/techarticles/pickle | xargs rm -f -r
     rm /media/diego/QData/techarticles/models.tgz
     tar cvfz /media/diego/QData/techarticles/models.tgz /media/diego/QData/techarticles/models
fi
if [ $? -eq 0 ] ; then
    ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/doc2vec | xargs rm -f -r'
    ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/lsi | xargs rm -f -r'
    ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/phrases | xargs rm -f -r'
    ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/pickle | xargs rm -f -r'
end
if [ $? -eq 0 ] ; then
    ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/doc2vec | xargs rm -f -r'
    ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/lsi | xargs rm -f -r'
    ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/phrases | xargs rm -f -r'
    ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/pickle | xargs rm -f -r'
end
if [ $? -eq 0 ] ; then
    ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/doc2vec | xargs rm -f -r'
    ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/lsi | xargs rm -f -r'
    ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/phrases | xargs rm -f -r'
    ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/pickle | xargs rm -f -r'
end
