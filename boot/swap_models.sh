find /media/diego/QData/techarticles/models/doc2vec -mtime +2 -type d | xargs rm -f -r
find /media/diego/QData/techarticles/models/lsi -mtime +2 -type d | xargs rm -f -r
find /media/diego/QData/techarticles/models/phrases -mtime +2 -type d | xargs rm -f -r
find /media/diego/QData/techarticles/pickle -mtime +2 | xargs rm -f -r
pushd /media/diego/QData; tar xvf techarticles.tgz; popd
cp /media/diego/keys/db_coords.yml /media/diego/QData/techarticles/keys/db_coords.yml
pkill gunicorn
cd /home/ubuntu/projects/newscollection/
sleep 30
/home/ubuntu/projects/newscollection/restart_app.sh
