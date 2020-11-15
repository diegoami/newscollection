LOG_LEVEL = 'INFO'

SPIDER_MODULES = ['technews_nlp_aggregator.scraping.main.scrapy.spiders']
NEWSPIDER_MODULE = 'technews_nlp_aggregator.scraping.main.scrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
#USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
USER_AGENT = 'Techcontroversy-TechcontroversyCrawler (root@techcontroversy.com)'


# Obey robots.txt rules
# ROBOTSTXT_OBEY = False
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#   'Accept-Encoding': 'gzip, deflate, br'
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapy.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrapy.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# DOWNLOADER_MIDDLEWARES = {
#
#         'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
#        'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
#        'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
#         'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None,
#        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
#         'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
#         'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
#        'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
#         'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
#         'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
#         'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
#        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
#         'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
#         'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
#
#
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

BOT_NAME = 'tnaggregator'

ITEM_PIPELINES = {
    'technews_nlp_aggregator.scraping.main.scrapy.Pipeline': 300,
}

