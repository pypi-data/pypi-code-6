#coding=utf-8
"""
example:

from walleclient import Client

client = Client()
client.avator_send(url = 'http://tp4.sinaimg.cn/2610171455/180/0/0',
                   uid = 'b703835eaa63fc8f8b609bfd4f475445')

"""
__author__ = 'ldd'
__version__ = '0.5.0'


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
        """
        params:  uid, locparam, lat, lng, accuracy
        """
        return self.impl.put('geo', version, params)

    def geo_send(self, uid, locparam, lat, lng, accuracy=None, version='1.0.0'):
        """ wrap up geo_put"""
        params = {}
        if lat and lng:
            params.update({
                'lat': lat,
                'lng': lng,
            })
        if locparam:
            params.update({'locparam': locparam})
        if params:
            params.update({'uid': uid})
            if accuracy:
                params.update({'accuracy': accuracy})
            return self.geo_put(params=params)
        else:
            return None

    def geo_ip_put(self, version='0.0.1', params={}):
        """
        params:  uid, ip
        """
        return self.impl.put('geo_ip', version, params)

    def geo_ip_send(self, uid, ip, version='1.0.0'):
        """ wrap up geo_ip_put"""
        params = {'uid': uid, 'ip': ip}
        return self.geo_ip_put(params=params)

    def avator_put(self, version='0.0.1', params={}):
        """
        params: {'uid': '', 'url': ''}
        """
        return self.impl.put('avator', version, params)

    def avator_send(self, uid, url):
        """ wrap up avator_put"""
        params = {'uid': uid, 'url': url}
        return self.avator_put(params=params)


class BeanstalkClient(object):
    def __init__(self, host, port):
        #self.conn = BeanConnection(host=host, port=port)
        self.host = host
        self.port = port
        self.conns = {}

    def get_connection(self, service):
        conn = self.conns.get(service)
        if conn is None:
            conn = BeanConnection(host=self.host, port=self.port)
            conn.use(service)
            self.conns[service] = conn
        return conn

    def put(self, service, version='0.0.1', params={}, level=JobLevel.Common, ttr=TimeOut):
        conn = self.get_connection(service)
        return conn.put(
            json.dumps({'service': service, 'version': version, 'params': params}),
            priority=level,
            ttr=ttr)
