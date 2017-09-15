git clone git@github.com:diegoami/newscollection.git
cd /app/newscollection/scrapers
git clone git@github.com:diegoami/techcrunch-posts-scraper.git
cd /app/newscollection/scrapers/techcrunch-posts-scraper
python  scrape.py
git add *
git  commit -a -m "Latest News"
git  push origin master
