import os
from .common import mkdir, create_file, add_poetry_script, extract_names, str_format
from .cmd import generate_cmd


def generate_scrapy(project_dir: str, package_dir: str, override: bool = False, *args, **kwargs):
    """生成scrapy模板代码"""
    # scrapy项目名称
    name = package_dir.replace('\\', '/').rstrip('/').split('/')[-1]
    class_name_prefix = ''.join([(n[0].upper() + n[1:]) if len(n) > 1 else n.upper() for n in extract_names(name)])

    def gen_scrapy_cfg():
        """生成scrapy.cfg文件"""
        scrapy_cfg = project_dir + os.sep + 'scrapy.cfg'
        create_file(scrapy_cfg, '''# Automatically created by: scrapy startproject
#
# For more information about the [deploy] section see:
# https://scrapyd.readthedocs.io/en/latest/deploy.html

[settings]
default = src.{name}.scrapy.settings

[deploy]
#url = http://localhost:6800/
project = {name}
'''.format(name=name), override=override)

    def gen_scrapy_dir():
        """生成scrapy目录"""
        scrapy_dir = package_dir + os.sep + 'scrapy'
        scrapy_init_py = scrapy_dir + os.sep + '__init__.py'
        items_py = scrapy_dir + os.sep + 'items.py'
        middlewares_py = scrapy_dir + os.sep + 'middlewares.py'
        pipelines_py = scrapy_dir + os.sep + 'pipelines.py'
        settings_py = scrapy_dir + os.sep + 'settings.py'
        spiders_dir = scrapy_dir + os.sep + 'spiders'
        spiders_init_py = spiders_dir + os.sep + '__init__.py'
        mkdir(scrapy_dir)
        create_file(scrapy_init_py, override=override)
        create_file(items_py, '''# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class {class_name_prefix}Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
'''.format(class_name_prefix=class_name_prefix), override=override)
        create_file(middlewares_py, '''# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class {class_name_prefix}SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class {class_name_prefix}DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
'''.format(class_name_prefix=class_name_prefix), override=override)
        create_file(pipelines_py, '''# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class {class_name_prefix}Pipeline:
    def process_item(self, item, spider):
        return item
'''.format(class_name_prefix=class_name_prefix), override=override)
        create_file(settings_py, str_format('''# Scrapy settings for ${name} project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "${name}"

SPIDER_MODULES = ["${name}.scrapy.spiders"]
NEWSPIDER_MODULE = "${name}.scrapy.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "${name} (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "${name}.scrapy.middlewares.${class_name_prefix}SpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "${name}.scrapy.middlewares.${class_name_prefix}DownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "${name}.scrapy.pipelines.${class_name_prefix}Pipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
''', name=name, class_name_prefix=class_name_prefix), override=override)
        mkdir(spiders_dir)
        create_file(spiders_init_py, '''# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
''', override=override)

    def gen_scrapy_ext():
        """生成scrapy拓展"""
        logger_dir = package_dir + os.sep + 'logger'
        logger_setup_py = logger_dir + os.sep + 'scrapy_setup.py'
        create_file(logger_setup_py, '''import logging
from logging.handlers import TimedRotatingFileHandler
from seatools.logger import get_loguru_adapter_logging_formatter
from {{cookiecutter.package_name}}.utils import get_log_path
from {{cookiecutter.package_name}}.config import cfg


def setup_scrapy(file_name,
                 rotation_type: str = 'd',
                 rotation: int = 1,
                 serialize: bool = True,
                 retention_count: int = 3,
                 level: str = 'INFO',
                 label=''):
    """设置scrapy日志记录, 与loguru相同的日志格式"""
    # 开启序列化则注入
    if serialize:
        # 增加一个适配loguru序列化的日志格式化器
        formatter_cls = get_loguru_adapter_logging_formatter()
        # 增加一个文件handler
        file_handler = TimedRotatingFileHandler(
            filename=get_log_path(file_name),
            when=rotation_type,
            interval=rotation,
            backupCount=retention_count,
            encoding='utf-8',
        )

        file_handler.setFormatter(
            formatter_cls('%(message)s', extra={'service_name': cfg().project_name, 'label': label}))
        file_handler.addFilter(lambda e: e.levelno >= logging._nameToLevel[level])
        logging_logger = logging.getLogger('scrapy')
        logging_logger.addHandler(file_handler)


def setup_scrapy_spider(file_name,
                        spider_name,
                        rotation_type: str = 'd',
                        rotation: int = 1,
                        serialize: bool = True,
                        retention_count: int = 3,
                        level: str = 'INFO',
                        label=''):
    """设置scrapy日志记录, 与loguru相同的日志格式"""
    # 开启序列化则注入
    if serialize:
        # 增加一个适配loguru序列化的日志格式化器
        formatter_cls = get_loguru_adapter_logging_formatter()
        # 增加一个文件handler
        file_handler = TimedRotatingFileHandler(
            filename=get_log_path(file_name),
            when=rotation_type,
            interval=rotation,
            backupCount=retention_count,
            encoding='utf-8',
        )

        file_handler.setFormatter(
            formatter_cls('%(message)s', extra={'service_name': cfg().project_name, 'label': label}))
        file_handler.addFilter(lambda e: e.levelno >= logging._nameToLevel[level])
        logging_logger = logging.getLogger(spider_name)
        logging_logger.addHandler(file_handler)
''', override=override)

    gen_scrapy_cfg()
    gen_scrapy_dir()
    gen_scrapy_ext()


def generate_scrapy_spider(project_dir: str, package_dir: str,
                           name: str, domain: str, override: bool = False, *args, **kwargs):
    """生成scrapy爬虫"""
    scrapy_dir = package_dir + os.sep + 'scrapy'
    if not os.path.exists(scrapy_dir):
        print('请先初始化scrapy项目结构后再生成爬虫')
        return
    if domain.startswith('http://'):
        domain = domain[7:]
    elif domain.startswith('https://'):
        domain = domain[8:]
    spiders_dir = scrapy_dir + os.sep + 'spiders'
    names = extract_names(name)
    spider_name = '_'.join(names)
    spider_class_name = ''.join([n.title() for n in names])
    spider_file = spiders_dir + os.sep + spider_name + '.py'
    create_file(spider_file, str_format("""from typing import Any

import scrapy
from scrapy.http.response import Response
from pathlib import Path
from demo_seatools.logger.scrapy_setup import setup_scrapy, setup_scrapy_spider


class ${class_name}Spider(scrapy.Spider):
    name = "${name}"
    allowed_domains = ["${domain}"]
    start_urls = ["https://${domain}"]

        def __init__(self, seatools_file_name=None, seatools_log_level=None, **kwargs: Any):
        super().__init__(**kwargs)
        setup_scrapy('{}.scrapy.log'.format(seatools_file_name), level=seatools_log_level, label='${name}')
        setup_scrapy_spider('{}.scrapy.{}.log'.format(seatools_file_name, self.name), self.name, level=seatools_log_level, label='${name}')

    def parse(self, response: Response, **kwargs: Any) -> Any:
        pass
""", name=spider_name, class_name=spider_class_name, domain=domain), override=override)
    # 生成完爬虫程序再生成cmd入口
    generate_cmd(project_dir, package_dir, override=override,
                 command=spider_name,
                 extra_import="from scrapy.cmdline import execute\n",
                 extra_run=str_format("execute(['scrapy', 'crawl', '${name}', '-a', 'seatools_file_name={}'.format(file_name), '-a', 'seatools_log_level={}'.format(log_level)])", name=spider_name))
