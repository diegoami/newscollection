#!/bin/bash
rm /media/diego/QData/techarticles.tgz
export PATH="/home/ubuntu/anaconda3/bin:$PATH"
export PATH="/home/ubuntu/.local/bin:$PATH"
cd /home/ubuntu/awscli/
/home/ubuntu/.local/bin/aws ec2 start-instances --instance-ids $1
EC2_PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $1  --query 'Reservations[*].Instances[*].PublicIpAddress' | egrep "[\d\.]+" | tr '"' ' ' | tr -d '[:space:]')
sleep 50m
while [ ! -f /media/diego/QData/techarticles.tgz ]
do
  sleep 1m
done
while [ ! $(wc -c <"/media/diego/QData/techarticles.tgz") -ge 1200000000 ]
do
  sleep 3m
done
/home/ubuntu/.local/bin/aws ec2 stop-instances --instance-ids $1
/home/ubuntu/awscli/swap_models.sh
#/home/ubuntu/projects/faqdomain_PY/src/restart_app.sh
