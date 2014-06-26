#coding=utf-8
__author__ = 'ldd'

__version__ = '0.2.0'


import json
from beanstalkc import Connection as BeanConnection

TimeOut = 60 * 10

class JobLevel:
    """ priority of job"""
    Critical = 32
    Urgent = 64
    Common = 1024
    Other = 2048

DefaultHost = "walle.oupeng.com"
DefaultPort = 11300

class Client(object):
    def __init__(self, host=DefaultHost, port=DefaultPort):
        self.impl = BeanstalkClient(host=host, port=port)

    def put(self, service, version='0.0.1', params={}, level=JobLevel.Common, time_out=TimeOut):
        return self.impl.put(service, version, params, level, time_out)

    def geo_put(self, version='0.0.1', params={}):
        return self.impl.put('geo', version, params)

    def avator_put(self, version='0.0.1', params={}):
        return self.impl.put('avator', version, params)


class BeanstalkClient(object):
    def __init__(self, host, port):
        self.conn = BeanConnection(host=host, port=port)
        self.conn.use('walle_worker')

    def put(self, service, version='0.0.1', params={}, level=JobLevel.Common, ttr=TimeOut):
        return self.conn.put(
            json.dumps({'service': service, 'version': version, 'params': params}),
            priority=level,
            ttr=ttr)


def test():
    client = Client()
    print client.geo_put()


if __name__ == '__main__':
    test()
