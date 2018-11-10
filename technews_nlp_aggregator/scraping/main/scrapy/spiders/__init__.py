# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from .util import extract_date, end_condition, build_text_from_paragraphs, get_date_from_string, already_crawled, build_from_timestamp, get_date_from_string_mdy, get_simple_date
from .tech_controversy_spider import TechControversySpider
from .arstechnica import ArstechnicaSpider
from .techcrunch import TechcrunchSpider
from .thenextweb import ThenextwebSpider
from .theverge import ThevergeSpider
from .venturebeat import VenturebeatSpider
from .techrepublic import TechrepublicSpider
from .wired import WiredSpider
from .engadget import EngadgetSpider
from .gizmodo import GizmodoSpider
from .mashable import MashableSpider
from .zdnet import ZdnetSpider
from .digitaltrends import DigitaltrendsSpider
from .theguardian import TheguardianSpider
from .qz import QzSpider
from .inquisitr import InquisitrSpider
from .recode import RecodeSpider
from .reuters import ReutersSpider
from .techdirt import TechdirtSpider
from .inverse import InverseSpider
from .bleepingcomputer import BleepingcomputerSpider
from .inc import IncSpider


