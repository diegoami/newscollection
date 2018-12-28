#!/bin/bash
rm /media/diego/QData/techarticles.tgz
export PATH="/home/ubuntu/anaconda3/bin:$PATH"
export PATH="/home/ubuntu/.local/bin:$PATH"
cd /home/ubuntu/awscli/
/home/ubuntu/.local/bin/aws ec2 start-instances --instance-ids $1
sleep 2m
EC2_PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $1  --query 'Reservations[*].Instances[*].PublicIpAddress' | egrep "[\d\.]+" | tr '"' ' ' | tr -d '[:space:]')
ssh ubuntu@$EC2_PUBLIC_IP -o StrictHostKeyChecking=no /bin/bash ssh_tc.sh 2>&1 >> /home/ubuntu/awscli/do_aws_3.log
/home/ubuntu/.local/bin/aws ec2 stop-instances --instance-ids $1
/home/ubuntu/awscli/swap_models.sh
