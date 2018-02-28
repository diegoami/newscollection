
source activate tnaggregator-3
nohup   gunicorn boot_web:app --timeout 120 --bind=0.0.0.0:8080 -w 1 --error-logfile=gunicorn-error.log --access-logfile=gunicorn-access.log &
