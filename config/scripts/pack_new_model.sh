cd /home/ubuntu/projects/newscollection/

find /media/diego/QData/techarticles/models/doc2vec -mmin +240  -type d | xargs rm -f -r
find /media/diego/QData/techarticles/models/lsi -mmin +240 -type d | xargs rm -f -r
find /media/diego/QData/techarticles/models/phrases -mmin +240 -type d | xargs rm -f -r
rm /media/diego/QData/techarticles/pickle/bigrams*
rm /media/diego/QData/techarticles/pickle/trigrams*
rm -rf /media/diego/QData/techarticles/keys/
find /media/diego/QData/techarticles/pickle/ -name texts_*.p -mmin +240 | xargs -n1 rm
rm /media/diego/QData/techarticles.tgz
pushd /media/diego/QData/
tar cvfz techarticles.tgz techarticles
popd
