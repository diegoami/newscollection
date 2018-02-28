#!/bin/bash
cd /home/ubuntu/projects/newscollection/
source /home/ubuntu/anaconda3/bin/activate tnaggregator-3

[ $? -eq 0 ] &&  python create_train_data.py $1
[ $? -eq 0 ] &&  python do_boost.py $1
[ $? -eq 0 ] &&  python create_test_data.py $1
[ $? -eq 0 ] &&  python do_predict.py $1
