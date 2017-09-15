FROM python:latest

MAINTAINER Diego Amicabile <diego.amicabile@gmail.com>

WORKDIR /app

ADD . /app

RUN mkdir ~/.ssh && cp /app/id_rsa ~/.ssh/ && cp /app/id_rsa.pub ~/.ssh/ && cp /app/known_hosts ~/.ssh/

RUN pip install -r requirements.txt

CMD ["bash",  "update_news.sh"]



