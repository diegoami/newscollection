#!/bin/bash
source /home/ubuntu/anaconda3/bin/activate tnaggregator-4
FDTIME="$(date +%y-%m-%d-%H-%M)"
/usr/bin/mysqldump --result-file=/media/diego/dumps/dump-$FDTIME.sql --databases tnaggregator --user=diegoami --password=$DB_PASSWORD --host=$DB_HOST
pushd /media/diego/dumps
tar cvfz dump-$FDTIME.sql.tgz dump-$FDTIME.sql
[ $? -eq 0 ] && /home/ubuntu/.local/bin/aws s3 rm s3://techcontroversy/dump-*.sql.tgz 
/home/ubuntu/.local/bin/aws s3 cp dump-$FDTIME.sql.tgz s3://techcontroversy/dump-$FDTIME.sql.tgz
rm dump-$FDTIME.sql.tgz
rm dump-$FDTIME.sql
popd
