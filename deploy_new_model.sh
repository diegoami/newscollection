ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/doc2vec -mtime +3 -type d | xargs rm -f -r'
ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/lsi -mtime +3 -type d | xargs rm -f -r'
ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/phrases -mtime +3 -type d | xargs rm -f -r'
ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/pickle | xargs rm -f -r'
ssh ubuntu@18.194.147.93 'rm /media/diego/QData/techarticles.tgz'
scp /media/diego/QData/techarticles.tgz ubuntu@18.194.147.93:/media/diego/QData
ssh ubuntu@18.194.147.93 'pushd /media/diego/QData; tar xvf techarticles.tgz; popd'