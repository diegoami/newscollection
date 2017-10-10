import yaml
config = yaml.safe_load(open('config.yml'))

root_dir        =  config['root_dir']
raw_base_dir    =  config['raw_base_dir']
parsed_base_dir =  config['parsed_base_dir']
link_file       =  config['link_file']
pattern         =  config['search_pattern']
connection_url  =  config['db_url']

from technews_nlp_aggregator.scraping.google_search_wrapper import Iterator
from technews_nlp_aggregator.scraping.technews_retriever import Converter

link_json = {}


iterator = Iterator(pattern)
iterator.load()
converter = Converter(db_connection=connection_url, iterator=iterator, raw_base_dir=raw_base_dir)
converter.convert_articles()
