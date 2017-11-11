source activate tnaggregator-2
cd projects/newscollection
pkill gunicorn
sleep(5)
python similar_articles_eff.py
nohup gunicorn boot_web:app --timeout 120 --bind=0.0.0.0:8080 -w 1 --error-log=gunicorn-error.log --access-log=gunicorn-access.log &
