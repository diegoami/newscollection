import json
import os
import sys
import yaml
import logging
from kafka import KafkaConsumer
MAX_SUBMITTED=1000

from technews_nlp_aggregator.persistence.articles_spider_repo import ArticlesSpiderRepo
from technews_nlp_aggregator.common import load_config
consumer = None
topic = None


if __name__ == "__main__":
    config = load_config(sys.argv)
    go_back = config["go_back"]
    db_config = yaml.safe_load(open(config["key_file"]))
    db_url = db_config["db_url"]
    logging.info("DB_URL: {}".format(db_url))
    articleSpiderRepo = ArticlesSpiderRepo(db_config.get("db_url"))

    consumer = KafkaConsumer(bootstrap_servers=f'kafka:9092',
                             auto_offset_reset='earliest',
                             enable_auto_commit=False,
                             group_id='my-group',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')));
    topic = 'Techcontroversy'
    consumer.subscribe(topic)
    for message in consumer:
       url = message.value['url']
       print(f'Adding url {url}')
       articleSpiderRepo.add_url_list([url])
