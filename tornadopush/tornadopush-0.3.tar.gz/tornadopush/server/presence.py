from tornado.websocket import WebSocketHandler
from .base import *


CONNECTED_USERS = {}


class PresenceMixin(object):
    def notify_join(self):
        self.user_meta = "{}"
        CONNECTED_USERS.setdefault(self.channel, {})
        if self.user_id:
            CONNECTED_USERS[self.channel][self.user_id] = self
            self.broadcast_presence_change("+")
            logger.debug('Presence: %s joined' % self.user_id)
        if CONNECTED_USERS[self.channel]:
            for handler in CONNECTED_USERS[self.channel].itervalues():
                self.handle_presence("+" + handler.format_presence_change_msg())

    def notify_leave(self):
        CONNECTED_USERS.setdefault(self.channel, {}).pop(self.user_id, None)
        self.broadcast_presence_change("-")
        logger.debug('Presence: %s left' % self.user_id)

    def on_presence_message(self, msg):
        if msg.startswith('bcast:'):
            logger.debug('Presence: broadcast from #%s: %s' % (self.user_id, msg[6:]))
            self.broadcast_presence_msg("%s;%s" % (self.user_id, msg[6:]))
        elif msg.startswith('meta:'):
            self.user_meta = msg[5:]
            logger.debug('Presence: meta for #%s: %s' % (self.user_id, self.user_meta))
            self.broadcast_presence_change("+")

    def broadcast_presence_msg(self, msg):
        for user_id, handler in CONNECTED_USERS[self.channel].iteritems():
            if user_id != self.user_id and handler.ws_connection:
                handler.handle_presence_broadcast(msg)

    def broadcast_presence_change(self, op):
        for user_id, handler in CONNECTED_USERS[self.channel].iteritems():
            if user_id != self.user_id and handler.ws_connection:
                handler.handle_presence(op + self.format_presence_change_msg())

    def format_presence_change_msg(self):
        return "%s;%s" % (self.user_id, self.user_meta)

    def handle_presence(self, msg):
        self.write_message("presence:%s" % msg)

    def handle_presence_broadcast(self, msg):
        self.write_message("presence_bcast:%s" % msg)


class PresenceHandler(PresenceMixin, ChannelMixin, AuthentifyMixin,\
                      WebSocketMixin, WebSocketHandler):

    def __init__(self, *args, **kwargs):
        WebSocketHandler.__init__(self, *args, **kwargs)
        self.create_client()

    def open(self, channel=""):
        self.channel = channel
        self.authentify(self.get_argument('token', None))

    def on_authorize(self):
        self.notify_join()

    def on_message(self, message):
        if message.startswith('presence:'):
            self.on_presence_message(message[9:])

    def on_close(self):
        self.notify_leave()