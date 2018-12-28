echo "EXECUTION OF TECHCONTROVERSY BATCH STARTED"
[ $? -eq 0 ] && mkdir /media/diego/QData/techarticles/keys/
[ $? -eq 0 ] && cp /media/diego/keys/db_coords.yml /media/diego/QData/techarticles/keys/db_coords.yml
[ $? -eq 0 ] && /home/ubuntu/projects/newscollection/update_model.sh
[ $? -eq 0 ] && /home/ubuntu/projects/newscollection/update_boost.sh
[ $? -eq 0 ] && /home/ubuntu/projects/newscollection/pack_new_model.sh
[ $? -eq 0 ] && /media/diego/scripts/dump_db_tnagg.sh
[ $? -eq 0 ] && /media/diego/scripts/copy_models_to_s3.sh
[ $? -eq 0 ] && /home/ubuntu/projects/newscollection/deploy_new_model.sh
exit $?

