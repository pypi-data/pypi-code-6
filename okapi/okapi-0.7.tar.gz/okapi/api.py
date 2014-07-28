# Copyright 2014 Red Beacon, Inc.  All Rights Reserved
#
# This code, and all derivative work, is the exclusive property of
# Red Beacon, Inc. and may not be used without Red Beacon, Inc.'s
# authorization.
#
# Author: Gobind Ball

"""
okapi.api
~~~~~~~~~
This module implements the Requests API while storing valuable information into mongodb.
"""

import datetime
import logging
import requests
import time
import urlparse

from pymongo import errors
from pymongo import MongoClient

logger = logging.getLogger(__name__)

# TODO:
# Depends on how we want to calculate the time to
# receieve the request form Home Depots API.
# There are several choices.
# Time.time, Time.clock, and a class from request called elapsed
# I have a test file that makes it seem that time.clock is fastest but is it most accurate?!?
# I have used time.clock for now

class Api(object):

    def __init__(self, project_name, mongodb_uri='mongodb://localhost'):
        """Initialization of class api.

        See http://docs.mongodb.org/manual/reference/connection-string/ for
        more information about the mongodb_uri parameter.
        """
        self.project_name = project_name

        try:
            client = MongoClient(mongodb_uri)
            self.db = client.okapi
        except (errors.ConnectionFailure, errors.InvalidURI):
            self.db = None
            logger.error('Unable to connect to MongoDB at %s', mongodb_uri)

    def request(self, method, url, **kwargs):
        """calls a method of request library while storing info about api call into mongo db"""
        content = ''
        status_code = None
        start = time.clock()
        try:
            res = requests.request(method, url, **kwargs)
            status_code = res.status_code
            if not res.ok:
                content = res.content
        except requests.exceptions.ConnectionError:
            content = 'Connection error'
        except requests.exceptions.HTTPError:
            content = 'HTTP error'
        except requests.exceptions.Timeout:
            content = 'Timeout'
        finally:
            end = time.clock()

        if self.db is not None:

            date = datetime.datetime.utcnow()
            host = urlparse.urlparse(url)

            data = {'content': content,
                    'date': date,
                    'host': host.hostname,
                    'method': method,
                    'project_name': self.project_name,
                    'response_time': (end - start),
                    'status_code': status_code,
                    'url': url,
            }

            try:
                datas = self.db.datas
                datas.insert(data)
            except errors.AutoReconnect:
                logger.error('Unable to connect to MongoDB '
                             'while trying to log a request')

        return res

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)
