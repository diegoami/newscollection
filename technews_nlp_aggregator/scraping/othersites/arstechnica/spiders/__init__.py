# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from .util import extract_date
from .arstechnica import ArstechnicaSpider
from .techcrunch import TechcrunchSpider
from .thenextweb import ThenextwebSpider
from .theverge import ThevergeSpider

