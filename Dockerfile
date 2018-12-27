FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade
RUN python3.6 -m pip install wheel

RUN apt-get install -y build-essential gcc libmysqlclient-dev mysql-client
COPY requirements.txt app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
RUN python3.6 -m spacy download en

RUN mkdir -p /media/diego/QData/techarticles/keys/
RUN mkdir ~/.aws

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG DB_URL
ARG ARCHIVE_NAME
ARG SECRET_KEY
ARG SIGNIN_KEY

RUN echo "[default]" >> ~/.aws/credentials
RUN echo "aws_access_key_id=$AWS_ACCESS_KEY_ID" >> ~/.aws/credentials
RUN echo "aws_secret_access_key=$AWS_SECRET_ACCESS_KEY" >> ~/.aws/credentials

RUN aws s3 cp $ARCHIVE_NAME /media/diego/QData/techcontroversy.tgz
RUN tar xvf /media/diego/QData/techcontroversy.tgz -C /media/diego/QData/

RUN echo "db_url : $DB_URL" >> /media/diego/QData/techarticles/keys/db_coords.yml
RUN echo "secret_key : $SECRET_KEY" >> /media/diego/QData/techarticles/keys/db_coords.yml
RUN echo "signin_key : $SIGNIN_KEY" >> /media/diego/QData/techarticles/keys/db_coords.yml

COPY . /app
EXPOSE 8081
EXPOSE 8080



