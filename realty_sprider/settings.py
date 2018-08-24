# -*- coding: utf-8 -*-


BOT_NAME = 'realty_sprider'
SPIDER_MODULES = ['realty_sprider.spiders']
NEWSPIDER_MODULE = 'realty_sprider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'realty_sprider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'realty_sprider.middlewares.RealtySpriderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

DOWNLOADER_MIDDLEWARES = {
   'realty_sprider.middlewares.RealtySpriderDownloaderMiddleware': 543,
   'realty_sprider.middlewares.UserAgentmiddleware': 600,
   # 'realty_sprider.middlewares.proxiesSpiderMiddleware': 600,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# MYEXT_ENABLED=True      # 开启扩展
# IDLE_NUMBER=30         # 配置空闲持续时间单位为 360个 ，一个时间单位为5s
#
# EXTENSIONS = {
#    # 'scrapy.extensions.telnet.TelnetConsole': None,
#    'realty_sprider.extensions.RedisSpiderSmartIdleClosedExensions': 500,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'realty_sprider.pipelines.RealtySpriderPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

# #将清除的项目在redis进行处理
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 300
# }

#Mysql数据库的配置信息
# MYSQL_HOST = 'localhost'
# MYSQL_DBNAME = 'emma'
# MYSQL_USER = 'root'
# MYSQL_PASSWD = 'root'
# MYSQL_PORT = 3306
TOTAL_PAGE=106

# postgresql
POSTGRESQL_HOST='**************'
POSTGRESQL_DBNAME = '**********'
POSTGRESQL_USER = '**********'
POSTGRESQL_PASSWD = '********************'
POSTGRESQL_PORT = 5433


#启用Redis调度存储请求队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#确保所有的爬虫通过Redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 允许暂停，redis请求记录不丢失
SCHEDULER_PERSIST = True

# 默认的scrapy-redis请求队列形式（按优先级）
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"

REDIS_HOST='****************'
REDIS_PORT=6379
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

