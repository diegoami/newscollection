#!/bin/bash
source /home/ubuntu/anaconda3/bin/activate tnaggregator-4
FDTIME="$(date +%y-%m-%d-%H-%M)"
TCHART=/media/diego/QData/techarticles.tgz
[ -e $TCHART ] && /home/ubuntu/.local/bin/aws s3 rm s3://techcontroversy/techarticles-*.tgz
/home/ubuntu/.local/bin/aws s3 cp $TCHART s3://techcontroversy/techarticles-$FDTIME.tgz
