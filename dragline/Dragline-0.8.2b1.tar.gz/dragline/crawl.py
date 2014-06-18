import json
import re
from defaultsettings import CrawlSettings, RequestSettings
from defaultsettings import SpiderSettings, LogSettings
import redisds
from http import Request, RequestError


class Crawl:
    settings = CrawlSettings()

    def __init__(self, spider):
        redis_args = dict(host=self.settings.REDIS_URL,
                          port=self.settings.REDIS_PORT,
                          db=self.settings.REDIS_DB)
        self.url_set = redisds.Set('urlset', spider._name, **redis_args)
        self.url_queue = redisds.Queue('urlqueue', spider._name, json,
                                       **redis_args)
        self.running_count = redisds.Counter("count", namespace=spider._name,
                                             **redis_args)
        self.allowed_urls_regex = re.compile(spider._allowed_urls_regex)
        self.spider = spider
        self.start()

    def start(self):
        request = self.spider._start
        if self.settings.MODE in ["NORM", "RESUME"]:
            if self.settings.MODE == "NORM":
                self.url_queue.clear()
                self.url_set.clear()
            self.running_count.set(0)
        if request.callback is None:
            request.callback = "parse"
        self.insert(request)

    def clear(self, finished):
        if self.settings.MODE == "NORM" or finished:
            self.url_queue.clear()
            self.url_set.clear()
        if self.settings.MODE != "DISTRIBUTE":
            self.running_count.set(0)

    def count(self):
        return self.running_count.get()

    def inc_count(self):
        self.running_count.inc()

    def decr_count(self):
        self.running_count.decr()

    def insert(self, request, check=True):
        if not isinstance(request, Request):
            return
        reqhash = request.get_unique_id()
        if check:
            if not self.allowed_urls_regex.match(request.url):
                return
            elif reqhash in self.url_set:
                return
        self.url_set.add(reqhash)
        self.url_queue.put(request.__dict__)
        del request


class Crawler():

    @classmethod
    def load_spider(Crawler, spider_class, settings):
        def get(value, default={}):
            try:
                return getattr(settings, value)
            except AttributeError:
                return default
        Crawl.settings = CrawlSettings(get('CRAWL'))
        Request.settings = RequestSettings(get('REQUEST'))
        spider_settings = SpiderSettings(get('SPIDER'))
        spider = spider_class(spider_settings)
        Crawler.log = LogSettings(get('LOGFORMATTERS'), get('LOGHANDLERS'),
                                  get('LOGGERS'))
        spider.logger = Crawler.log.getLogger(spider._name)
        Crawler.crawl = Crawl(spider)

    def process_url(self):
        crawl = Crawler.crawl
        logger = Crawler.log.getLogger("dragline")
        request = Request(None)
        while True:
            args = crawl.url_queue.get(timeout=2)
            if args:
                request._set_state(args)
                logger.info("Processing %s", request)
                crawl.inc_count()
                try:
                    response = request.send()
                    try:
                        callback = getattr(crawl.spider, request.callback)
                        if request.meta:
                            requests = callback(response, request.meta)
                        else:
                            requests = callback(response)
                    except:
                        logger.exception("Failed to execute callback")
                        requests = None
                    if requests:
                        for i in requests:
                            crawl.insert(i)
                except RequestError as e:
                    request.retry += 1
                    if request.retry >= crawl.settings.MAX_RETRY:
                        logger.warning("Rejecting %s", request)
                    else:
                        logger.debug("Retrying %s", request)
                        crawl.insert(request, False)
                except Exception as e:
                    logger.exception('Failed to open the url %s', request)
                else:
                    logger.info("Finished processing %s", request)
                finally:
                    crawl.decr_count()
            else:
                if crawl.count() == 0:
                    break
                logger.debug("Waiting for %s", crawl.count())
