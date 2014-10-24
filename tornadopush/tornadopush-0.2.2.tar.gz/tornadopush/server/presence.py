from tornado.websocket import WebSocketHandler
from .base import *


class PresenceMixin(object):
    @property
    def presence_users_key(self):
        return self.application.settings['presence_users_key'] % self.channel

    @property
    def presence_channel(self):
        return self.application.settings['presence_channel'] % self.channel

    def notify_join(self, callback=None):
        def on_members(members):
            if members:
                self.handle_presence("+" + ";+".join(members))
            if callback:
                callback()
        def list_members(*args):
            self.client.smembers(self.presence_users_key, on_members)
        def on_add(r):
            logger.debug('Presence: %s joined' % self.user_id)
            self.client.publish(self.presence_channel, "+%s" % self.user_id,
                list_members)
        if self.user_id:
            self.client.sadd(self.presence_users_key, self.user_id, callback=on_add)
        else:
            list_members()

    def notify_leave(self, callback=None):
        def on_published(r):
            logger.debug('Presence: %s left' % self.user_id)
            if callback:
                callback()
        def on_removed(r):
            self.client.publish(self.presence_channel,
                "-%s" % self.user_id, on_published)
        self.client.srem(self.presence_users_key, self.user_id, callback=on_removed)

    def handle_presence(self, msg):
        raise NotImplementedError


class PresenceHandler(PresenceMixin, ChannelMixin, AuthentifyMixin, BrukvaMixin,\
                      WebSocketMixin, WebSocketHandler):

    def __init__(self, *args, **kwargs):
        WebSocketHandler.__init__(self, *args, **kwargs)
        self.create_client()

    def open(self, channel=""):
        self.channel = channel
        self.authentify(self.get_argument('token', None))

    def on_authorize(self):
        self.notify_join(lambda: self.subscribe(self.presence_channel))

    def on_message(self, message):
        pass

    def on_redis_message(self, msg):
        self.handle_presence(str(msg.body))

    def handle_presence(self, msg):
        self.write_message("presence:%s" % msg)

    def on_close(self):
        def on_unsubscribe():
            self.notify_leave(lambda: self.close_client())
        self.unsubscribe(on_unsubscribe)