#!/bin/bash

cd /home/ubuntu/projects/newscollection/
source /home/ubuntu/anaconda3/bin/activate tnaggregator-3
git pull origin spacy2
nohup /home/ubuntu/anaconda3/envs/tnaggregator-3/bin/gunicorn boot_web:app --timeout 120 --bind=0.0.0.0:8080 -w 1 --error-logfile=gunicorn-error.log --access-logfile=gunicorn-access.log &
