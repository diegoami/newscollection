# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from .util import extract_date, end_condition, build_text_from_paragraphs, get_date_from_string, already_crawled, build_from_timestamp, get_date_from_string_mdy, get_simple_date
from .tech_controversy_spider import TechControversySpider
from .arstechnica import ArstechnicaSpider
from .bleepingcomputer import BleepingcomputerSpider
from .cnbc import CnbcSpider
from .cnet import CnetSpider
from .digit_fyi import DigitSpider
from .digitaltrends import DigitaltrendsSpider
from .engadget import EngadgetSpider
from .forbes import ForbesSpider
from .gizmodo import GizmodoSpider
from .inc import IncSpider
from .inquisitr import InquisitrSpider
from .inverse import InverseSpider
from .mashable import MashableSpider
from .pcmag import PcmagSpider
from .qz import QzSpider
from .recode import RecodeSpider
from .reuters import ReutersSpider
from .techdirt import TechdirtSpider
from .technicalhint import TechnicalhintSpider
from .techrepublic import TechrepublicSpider
from .techtimes import TechtimesSpider
from .theguardian import TheguardianSpider
from .thenextweb import ThenextwebSpider
from .theverge import ThevergeSpider
from .venturebeat import VenturebeatSpider
from .wired import WiredSpider
from .zdnet import ZdnetSpider

all_spiders = [
    ArstechnicaSpider,
    BleepingcomputerSpider,
    CnbcSpider,
    CnetSpider,
    DigitSpider,
    DigitaltrendsSpider,
    EngadgetSpider,
    ForbesSpider,
    GizmodoSpider,
    IncSpider,
    InquisitrSpider,
    InverseSpider,
    MashableSpider,
    PcmagSpider,
    QzSpider,
    RecodeSpider,
    ReutersSpider,
    TechdirtSpider,
    TechnicalhintSpider,
    TechrepublicSpider,
    TechtimesSpider,
    TheguardianSpider,
    ThenextwebSpider,
    ThevergeSpider,
    VenturebeatSpider,
    WiredSpider,
    ZdnetSpider]

all_domains = [domain for spider in all_spiders for domain in spider.allowed_domains ]
all_start_urls = [start_url for spider in all_spiders for start_url in spider.start_urls ]

