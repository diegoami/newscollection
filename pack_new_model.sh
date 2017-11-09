 rm /media/diego/QData/pickle/bigrams*
 rm /media/diego/QData/pickle/trigrams*
 find . -name "texts*.p" -mtime +1 | xargs -n1 rm
 rm /media/diego/QData/techarticles.tgz
 pushd /media/diego/QData/
 tar cvfz techarticles.tgz techarticles
 popd