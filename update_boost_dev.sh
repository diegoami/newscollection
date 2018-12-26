#!/bin/bash

[ $? -eq 0 ] &&  python create_train_data.py config_dev.yml
[ $? -eq 0 ] &&  python do_boost.py config_dev.yml
[ $? -eq 0 ] &&  python create_test_data.py config_dev.yml
[ $? -eq 0 ] &&  python do_predict.py config_dev.yml
