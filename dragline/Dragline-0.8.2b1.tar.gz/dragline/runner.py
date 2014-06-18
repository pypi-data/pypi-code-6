from gevent import monkey, spawn, joinall
monkey.patch_all()

import sys
import argparse
import os
import traceback
from defaultsettings import SpiderSettings, LogSettings
from crawl import Crawler


logger = LogSettings().getLogger("dragline")


def load_module(path, filename):
    try:
        sys.path.insert(0, path)
        module = __import__(filename)
        del sys.path[0]
        return module
    except Exception as e:
        logger.exception("Failed to load module %s" % filename)
        raise ImportError


def main(directory):
    settings_module = load_module(directory, "settings")
    spider_module = load_module(directory, "main")
    spider = getattr(spider_module, "Spider")
    Crawler.load_spider(spider, settings_module)
    crawlers = [Crawler() for i in xrange(5)]
    try:
        joinall([spawn(crawler.process_url) for crawler in crawlers])
    except KeyboardInterrupt:
        Crawler.crawl.clear(False)
    except:
        logger.exception("Unable to complete")
    else:
        Crawler.crawl.clear(True)
        logger.info("Crawling completed")


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('spider', help='spider directory name')
    args = parser.parse_args()
    path = os.path.abspath(args.spider)
    main(path)

if __name__ == "__main__":
    run()
