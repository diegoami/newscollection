
from technews_nlp_aggregator.scraping.google_search_wrapper import Command, create_google_service, Iterator
from technews_nlp_aggregator.scraping.technews_retriever import Raw_Retriever
import yaml

config = yaml.safe_load(open('config.yml'))

count = 0


exclusions = ["jp_techcrunch"]

it = Iterator( config['search_pattern'])
it.load()

raw_retr = Raw_Retriever( exclusions=exclusions, raw_base_dir=config['raw_base_dir'])

raw_retr.download_files(iterator=it)