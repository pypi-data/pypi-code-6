#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random
import time
import uuid
from kazoo.client import KazooClient


class ServiceDiscovery:

    def __init__(self, base_path, zoo_hosts):
        self.zk = KazooClient(hosts=zoo_hosts)
        self.zk.start()
        self.base_path = base_path
        self.package = base_path[3:]

    def register(self, service_name, address, port):
        """
        Register your service in service discovery
        :param service_name:
        :param address: hostname or IP
        :param port: HTTP port number
        :return: unique service id
        """
        instance_id = self._generate_unique_service_id()
        service_definition = self._create_instance_definition(self.package,
            service_name, address, port, instance_id,
            str(int(time.time() * 1000)))
        self.zk.ensure_path(self.base_path + "/" + service_name)
        self.zk.create(self.base_path + "/" + service_name + "/" + instance_id,
                    service_definition, ephemeral=True)
        return instance_id

    def _generate_unique_service_id(self):
        return str(uuid.uuid1())

    def get_instance(self, service_name):
        """
        Returns random service instance from service discovery
        :return: service url as string
        """
        return random.choice(self.get_instances(service_name))

    def get_instances(self, service_name):
        """
        Returns service instances registered in service discovery
        :return: service url as string
        """
        ids = self.zk.get_children(self.base_path + "/" + service_name)
        return [self._instance_url(
            self._get_instance_definition(service_name, id)) for id in ids]

    def _get_instance_definition(self, service_name, id):
        return self.zk.get(self.base_path + "/" + service_name + "/" + id)[0]

    @classmethod
    def _instance_url(cls, instance_definition):
        """
        :param instance_definition: service definition in JSON
        :return: url for instance as string

        >>> i_def = '{"name":"pl/microhackaton/twitter-collector",' \
        '"id":"03590c70-455a-4624-a6d7-1ac02fc0c9bc",' \
        '"address":"10.89.136.122","port":8081,"sslPort":null,"payload":null,' \
        '"registrationTimeUTC":1407577834980,"serviceType":"DYNAMIC",' \
        '"uriSpec":{"parts":[{"value":"scheme","variable":true},' \
        '{"value":"://","variable":false},{"value":"address","variable":true},' \
        '{"value":":","variable":false},{"value":"port","variable":true}]}}'
        >>> ServiceDiscovery._instance_url(i_def)
        u'http://10.89.136.122:8081'
        """
        instance_dict = json.loads(instance_definition)
        return "http://%(address)s:%(port)s" % instance_dict

    @classmethod
    def _create_instance_definition(cls, package, service_name,
                                    address, port, uuid, registration_timestamp):
        return '{"name":"%(package)s/%(service_name)s",' \
        '"id":"%(uuid)s",' \
        '"address":"%(address)s","port":%(port)s,"sslPort":null,"payload":null,' \
        '"registrationTimeUTC":%(registration_timestamp)s,"serviceType":"DYNAMIC",' \
        '"uriSpec":{"parts":[{"value":"scheme","variable":true},' \
        '{"value":"://","variable":false},{"value":"address","variable":true},' \
        '{"value":":","variable":false},{"value":"port","variable":true}]}}' % \
        locals()
