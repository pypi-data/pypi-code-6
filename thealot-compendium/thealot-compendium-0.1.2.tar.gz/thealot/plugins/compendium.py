from .plugin import Plugin

import threading
import requests
import time


class CompendiumPlugin(Plugin):

    URL = 'http://www.dota2.com/international/compendium/'
    DIV = 'Copy02_PP'
    TIMEOUT = 60
    THRESHOLD = -5  # Every $100,000
    MESSAGE = 'New amount reached: ${}'

    help = {
    }

    def hook(self):
        self.lastAmount = 0
        self.crawler = threading.Thread(target=self.crawl)
        self.running = True
        self.crawler.start()

    def unhook(self):
        self.running = False

    def crawl(self):
        while self.running:
            r = requests.get(CompendiumPlugin.URL)
            if r.status_code == requests.codes.ok:
                amount = self.findAmount(r.text)
                rounded = round(amount, CompendiumPlugin.THRESHOLD)

                if rounded > self.lastAmount:
                    self.lastAmount = rounded
                    print('Compendium.lastAmount => {}'.format(rounded))
                    self.announce(amount)
            time.sleep(CompendiumPlugin.TIMEOUT)

    def findAmount(self, html):
        start = html.find('$', html.find(CompendiumPlugin.DIV)+1) + 1
        end = html.find('<', start)
        return int(''.join(html[start:end].split(',')))

    def announce(self, amount):
        amount = self.intWithCommas(amount)
        channel = self.bot.config['channel']
        try:
            self.message(channel, CompendiumPlugin.MESSAGE.format(amount))
        except Exception:  # bad bad bad
            pass

    def __del__(self):
        self.unhook()

    def intWithCommas(self, x):
        """http://stackoverflow.com/a/1823101"""
        if x < 0:
            return '-' + self.intWithCommas(-x)
        result = ''
        while x >= 1000:
            x, r = divmod(x, 1000)
            result = ",%03d%s" % (r, result)
        return "%d%s" % (x, result)
