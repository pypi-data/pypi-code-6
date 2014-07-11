"""
This CityLink Utilities library was built to help integrate with ecommerce shops 
for easy updating of delivery statuses. As well as a few extras like emailing manifests.

Copyright (c) 2013-2014, Doug Bromley <doug.bromley@gmail.com>.
License: BSD (see LICENSE for details)
"""

from mechanize import Browser
from lxml import html
from mailer import Mailer
from mailer import Message

__author__ = "Doug Bromley"
__version__ = "0.8b"
__license__ = "BSD"

class CityLink(Browser, object):
    def __init__(self, username, password):
        super(CityLink, self).__init__()
        self.set_handle_robots(False)
        self.username = username
        self.password = password

        self.loginurl = "https://www.city-link.co.uk/log_in/log_in2.php?custno=%s&x=24&y=12" % self.username

        self.urls = {
            "customer": "http://www.city-link.co.uk/customer/",
            "login": self.loginurl,
            "pending": "https://www.city-link.co.uk/orders/web/todaysprintablejobs.php",
            "manifest": "https://www.city-link.co.uk/orders/web/manifest.php",
            "fullmanifest": "https://www.city-link.co.uk/orders/web/fullmanifest.php",
            "logout": "https://www.city-link.co.uk/log_in/log_out.php",
        }

    def login(self):
        """Login to the CityLink customer area and return resource"""
        self.open(self.urls['login'])
        self.select_form(nr=0)

        self.form['custno'] = self.username
        self.form['password'] = self.password
        res = self.submit()
        
        return res

    def logout(self):
        pass

    def fetch_pending(self):
        """Returns list of pending job references"""
        pending = self.open(self.urls['pending'])
        soup = BeautifulSoup(pending.read())

    def fetch_manifest(self):
        """Returns summary manifest page"""
        manifest = self.open(self.urls['manifest'])
        return manifest.read()
    
    def fetch_citylink_refs(self):
        """Grab the City Link reference numbers as a list"""
        tree = html.fromstring(self.fetch_manifest())
        self_refs = tree.xpath('//table/tr/td/table/tr[position()>4]/td[1]/text()')
        return [x.strip() for x in self_refs[:-1]]

    def fetch_self_refs(self):
        """Grab your reference numbers as a list"""
        tree = html.fromstring(self.fetch_manifest())
        self_refs = tree.xpath('//table/tr/td/table/tr[position()>4]/td[2]/text()')
        return [x.strip() for x in self_refs[:-1]]

    def mail_manifest(self, emailfrom, emailto):
        message = Message(From=emailfrom, To=emailto)
        message.Subject = "Manifest"
        message.Html = self.fetch_manifest()
        
        sender = Mailer('localhost')
        sender.send(message)
