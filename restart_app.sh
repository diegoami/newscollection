#!/bin/bash

cd /home/ubuntu/projects/newscollection/
source /home/ubuntu/anaconda3/bin/activate tnaggregator-4
git pull origin master
mkdir -p /media/diego/QData/techarticles/version
echo $(git log -n1 --pretty='%h') > /media/diego/QData/techarticles/version/frontend_version.txt

nohup /home/ubuntu/anaconda3/envs/tnaggregator-4/bin/gunicorn boot_web:app --timeout 480 --bind=0.0.0.0:8080 -w 1 --error-logfile=gunicorn-error.log --access-logfile=gunicorn-access.log &
pushd ../DA_praw_queue
docker-compose up -d
popd
nohup /home/ubuntu/anaconda3/envs/tnaggregator-4/bin/python consume.py &> consume.out &