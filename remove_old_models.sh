
 find /media/diego/QData/techarticles/models/doc2vec  -mtime +1 -type d | xargs rm -f -r
 find /media/diego/QData/techarticles/models/lsi -mtime +1 -type d | xargs rm -f -r
 find /media/diego/QData/techarticles/models/phrases -mtime +1 -type d | xargs rm -f -r
 find /media/diego/QData/techarticles/pickle -mtime +7 -type d | xargs rm -f -r
 rm /media/diego/QData/techarticles/models.tgz
 pushd /media/diego/QData/techarticles/
 tar cvfz models.tgz models
 popd