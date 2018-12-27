#!/bin/bash
source activate tnaggregator-4
FDTIME="$(date +%y-%m-%d-%H-%M)"
TCHART=/media/diego/QData/techarticles.tgz
[ -e $TCHART ] && aws s3 cp $TCHART s3://techcontroversy-dev/techarticles-$FDTIME.tgz
