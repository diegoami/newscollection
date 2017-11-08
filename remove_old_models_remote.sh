ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/doc2vec -mtime +3 -type d | xargs rm -f -r'
ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/lsi -mtime +3 -type d | xargs rm -f -r'
ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/models/phrases -mtime +3 -type d | xargs rm -f -r'
ssh ubuntu@18.194.147.93 'find /media/diego/QData/techarticles/pickle -mtime +7 -type d | xargs rm -f -r'
ssh ubuntu@18.194.147.93 'rm /media/diego/QData/techarticles/models.tgz'

