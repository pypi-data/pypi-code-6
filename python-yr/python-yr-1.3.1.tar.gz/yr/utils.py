#!/usr/bin/env python3

import sys
import os.path
import json # Language
import tempfile # Cache
import datetime # Cache
import urllib.request # Connect
import urllib.parse # Location

class YrObject: encoding = 'utf-8'

class YrException(YrObject):

    def __init__(self, error_message):
        sys.stderr.write('python-yr: {error_message}\n'.format(error_message=error_message))
        sys.exit(1)

class Language(YrObject):

    script_directory = os.path.dirname(os.path.abspath(__file__)) # directory of the script
    directory = 'languages'

    def __init__(self, language_name='en'):
        self.language_name = language_name
        self.filename = os.path.join(
            self.script_directory,
            self.directory,
            '{root}.{ext}'.format(root=self.language_name, ext='json') # basename of filename
        )
        self.dictionary = self.get_dictionary()

    def get_dictionary(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', encoding=self.encoding) as f:
                return json.load(f)
        else:
            YrException('unavailable language ~> {language_name}'.format(language_name=self.language_name))

class Location(YrObject):

    def __init__(self, location_name, language=Language()):
        self.location_name = location_name
        self.language = language
        self.url = self.get_url()
        self.hash = self.get_hash()

    def get_url(self):
        url = 'http://www.yr.no/{place}/{location_name}/{forecast}.xml'.format(
            location_name = urllib.parse.quote(self.location_name),
            **self.language.dictionary # **self.language.dictionary contain ~> place + forecast
        )
        return url

    def get_hash(self):
        return self.location_name.replace('/', '-')

class Connect(YrObject):

    def __init__(self, location):
        self.location = location

    def read(self):
        cache = Cache(self.location)
        if not cache.exists() or not cache.is_fresh():
            try:
                response = urllib.request.urlopen(self.location.url)
            except:
                YrException('unavailable url ~> {url}'.format(url=self.location.url))
            if response.status != 200:
                YrException('unavailable url ~> {url}'.format(url=self.location.url))
            weatherdata = response.read().decode(self.encoding)
            cache.dump(weatherdata)
        else:
            weatherdata = cache.load()
        return weatherdata

class Cache(YrObject):

    directory = tempfile.gettempdir()
    extension = 'weatherdata.xml'
    timeout = 30 # cache timeout in minutes

    def __init__(self, location):
        self.location = location
        self.filename = os.path.join(
            self.directory,
            '{root}.{ext}'.format(root=self.location.hash, ext=self.extension) # basename of filename
        )

    def dump(self, data):
        with open(self.filename, mode='w', encoding=self.encoding) as f:
            f.write(data)

    def is_fresh(self):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(self.filename))
        now = datetime.datetime.now()
        timeout = datetime.timedelta(minutes=self.timeout)
        return now - mtime <= timeout # thanks for the fix antorweep

    def exists(self):
        return os.path.isfile(self.filename)

    def load(self):
        with open(self.filename, mode='r', encoding=self.encoding) as f:
            return f.read()

if __name__ == '__main__':
    print(Connect(Location('Czech_Republic/Prague/Prague')).read())
