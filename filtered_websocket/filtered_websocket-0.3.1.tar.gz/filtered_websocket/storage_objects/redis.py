from __future__ import absolute_import

import redis
import redis_collections

from .base import BasePubSubStorageObject
from ..pubsub_listeners.redis import RedisPubSubListener


class StorageObject(BasePubSubStorageObject):

    def __init__(self, options, *args, **kwargs):
        super(StorageObject, self).__init__(options, *args, **kwargs)
        self.redis = redis.Redis(
            host=self.options.redis_host,
            port=self.options.redis_port
        )
        self.storage = redis_collections.Dict(
            key=self.options.redis_key,
            redis=self.redis
        )

    def get_client(self):
        return self.redis

    def get(self, item):
        return self.storage.get(item)

    def __getitem__(self, item):
        return self.get(item)

    def add(self, key, value):
        current = self.storage.get(key)
        if current is None:
            current = set()
        current.add(value)
        self.storage[key] = current

    def remove(self, key, item):
        current = self.storage.get(key)
        if current is not None:
            current.remove(item)
            self.storage[key] = current

    def publish(self, channel, data):
        self.redis.publish(channel, data)

    @classmethod
    def get_pubsub_listener(cls):
        return RedisPubSubListener

    @classmethod
    def parser(cls, parser):
        parser.add_argument(
            "--redis_host",
            default="localhost"
        )
        parser.add_argument(
            "--redis_port",
            type=int,
            default=6379
        )
        parser.add_argument(
            "--redis_channels",
            help="pubsub channels to subscribe to.",
            nargs="*"
        )
        parser.add_argument(
            "--redis_key",
            help="A key prefix.",
            default="my_app"
        )
        return parser
