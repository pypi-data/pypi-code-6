#!/usr/bin/env python
# encoding: utf-8
import pickle

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import getLogger


class Email(object):
    log = getLogger('emailer.email')
    def __init__(self, sender, recipient, subject, headers={}):
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = subject
        self.msg['From'] = sender
        self.msg['To'] = recipient
        self.log.debug("Building message from <{0}> to <{1}>".format(sender, recipient))
        for key, value in headers.iteritems():
            self.log.debug('Add header "{0}": "{1}"'.format(key, value))
            self.msg[key] = value

    def set_header(self, key, value):
        self.log.debug('Setting header "{0}": "{1}"'.format(key, value))
        self.msg[key] = value

    def get_header(self, key, default=None):
        if key in self.msg:
            return self.msg[key]
        else:
            return default

    def dumps(self):
        self.log.debug('Serializing message from <{0}> to <{1}>'.format(self.msg['From'], self.msg['To']))
        return pickle.dumps(self)

    def add_part(self, part, mimetype='plain'):
        prt = unicode(part)
        self.log.debug('Adding "{0}" (length: {3}) part to message from <{1}> to <{2}>'.format(mimetype, self.msg['From'], self.msg['To'], len(prt)))
        self.msg.attach(MIMEText(prt, mimetype, _charset='utf-8'))
