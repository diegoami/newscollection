
 find /media/diego/QData/techarticles/models/doc2vec   -type d | xargs rm -f -r
 find /media/diego/QData/techarticles/models/lsi -type d | xargs rm -f -r
 find /media/diego/QData/techarticles/models/phrases -type d | xargs rm -f -r
 find /media/diego/QData/techarticles/pickle -mtime +2 -type d | xargs rm -f -r
