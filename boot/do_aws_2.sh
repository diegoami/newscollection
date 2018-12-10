#!/bin/bash
rm /media/diego/QData/techarticles.tgz
export PATH="/home/ubuntu/anaconda3/bin:$PATH"
export PATH="/home/ubuntu/.local/bin:$PATH"
cd /home/ubuntu/awscli/
/home/ubuntu/.local/bin/aws ec2 start-instances --instance-ids $1
sleep 45m
while [ ! -f /media/diego/QData/techarticles.tgz ]
do
  sleep 1m
done
sleep 1m
/home/ubuntu/.local/bin/aws ec2 stop-instances --instance-ids $1
find /media/diego/QData/techarticles/models/doc2vec -mtime +3 -type d | xargs rm -f -r
find /media/diego/QData/techarticles/models/lsi -mtime +3 -type d | xargs rm -f -r
find /media/diego/QData/techarticles/models/phrases -mtime +3 -type d | xargs rm -f -r
find /media/diego/QData/techarticles/pickle -mtime +3 | xargs rm -f -r
pushd /media/diego/QData; tar xvf techarticles.tgz; popd
pkill gunicorn
cd /home/ubuntu/projects/newscollection/
git pull origin master
sleep 30
/home/ubuntu/projects/newscollection/restart_app.sh
