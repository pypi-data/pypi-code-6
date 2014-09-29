# -*- coding: utf-8 -*-
"""
docker_registry.drivers.manta
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a manta based driver.

"""

from docker_registry.core import driver
from docker_registry.core import exceptions
from docker_registry.core import lru
import os

from manta import PrivateKeySigner, MantaClient


class Storage(driver.Base):
    def __init__(self, path=None, config=None):
        self.config = config
        self.signer = PrivateKeySigner(key_id=config.key_id,
                                       priv_key=open(config.private_key).read())
        self.client = MantaClient(config.url, config.account, self.signer,
                                        disable_ssl_certificate_validation=config.insecure,
                                        cache_dir='/tmp')
        self.client.mkdirp(config.path)

    def create_manta_path(self, path=None):
        if path is None:
            return self.config.path % self.config.account
        return os.path.join(self.config.path % self.config.account, path)

    @lru.set
    def get_content(self, path):
        mpath = self.create_manta_path(path)
        try:
            return self.client.get_object(mpath)
        except Exception:
            raise exceptions.FileNotFoundError("File %s not found" % path)

    @lru.get
    def put_content(self, path, content):
        if not isinstance(content, bytes):
            content = bytes(content)

        mpath = self.create_manta_path(path)
        self.client.mkdirp(os.path.dirname(mpath))
        self.client.put_object(mpath, content=content, content_type='text/plain')

    def exists(self, path):
        mpath = self.create_manta_path(path)
        res, status = self.client._request(path=mpath, method='HEAD')
        return str(res.status) != '404'


    def stream_write(self, path, fp):
        mpath = self.create_manta_path(path)
        self.client.put_object(mpath, file=fp)

    def stream_read(self, path, bytes_range=None):
        mpath = self.create_manta_path(path)
        return self.client.get_object(mpath)

    def list_directory(self, path):
        mpath = self.create_manta_path(path)
        files = self.client.list_directory(mpath)
        objects = []
        for file in files:
            objects.append(os.path.join(path, file['name']))
        return objects

    @lru.remove
    def remove(self, path):
        mpath = self.create_manta_path(path)
        self.client.delete_object(mpath)

    def content_redirect_url(self, path):
        return self.config.url + path
