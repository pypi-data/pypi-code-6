from tornado.websocket import WebSocketHandler
from .base import *


CONNECTED_USERS = {}


class User(object):
    def __init__(self, uid, meta='{}'):
        self.uid = uid
        self.meta = meta
        self.handlers = []

    def handle_presence_broadcast(self, msg):
        for handler in self.handlers:
            if handler.ws_connection:
                handler.handle_presence_broadcast(msg)

    def handle_presence(self, msg):
        for handler in self.handlers:
            if handler.ws_connection:
                handler.handle_presence(msg)

    def format_presence_change_msg(self):
        return "%s;%s" % (self.uid, self.meta)


class PresenceMixin(object):
    def notify_join(self):
        self.user = None
        CONNECTED_USERS.setdefault(self.channel, {})
        if self.user_id:
            if not self.user_id in CONNECTED_USERS[self.channel]:
                CONNECTED_USERS[self.channel][self.user_id] = User(self.user_id)
            self.user = CONNECTED_USERS[self.channel][self.user_id]
            self.user.handlers.append(self)
            self.broadcast_presence_change("+")
            logger.debug('Presence: %s joined' % self.user_id)
        if len(CONNECTED_USERS[self.channel]) > 1:
            for user in CONNECTED_USERS[self.channel].itervalues():
                if user.uid != self.user_id:
                    self.handle_presence("+%s" % user.format_presence_change_msg())

    def notify_leave(self):
        if self.user:
            self.user.handlers.remove(self)
            if not self.user.handlers:
                CONNECTED_USERS[self.channel].pop(self.user_id)
                self.broadcast_presence_change("-")
                logger.debug('Presence: %s left' % self.user_id)

    def _broadcast(self, func, *args):
        for user in CONNECTED_USERS[self.channel].itervalues():
            if user.uid != self.user_id:
                getattr(user, func)(*args)

    def on_presence_message(self, msg):
        if msg.startswith('bcast:'):
            logger.debug('Presence: broadcast from #%s: %s' % (self.user_id, msg[6:]))
            self.broadcast_presence_msg("%s;%s" % (self.user_id, msg[6:]))
        elif msg.startswith('meta:'):
            self.user.meta = msg[5:]
            logger.debug('Presence: meta for #%s: %s' % (self.user_id, self.user.meta))
            self.broadcast_presence_change("+")

    def broadcast_presence_msg(self, msg):
        self._broadcast('handle_presence_broadcast', msg)

    def broadcast_presence_change(self, op):
        self._broadcast('handle_presence', op + self.user.format_presence_change_msg())

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