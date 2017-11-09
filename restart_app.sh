source activate tnaggregator-2
cd projects/newscollection
pkill gunicorn
sleep 10
nohup gunicorn boot_web:app --timeout 120 --bind=0.0.0.0:8080 -w 1 &
