from __future__ import absolute_import

from .base import WebSocketMessageFilter


class BroadcastMessagesFilter(WebSocketMessageFilter):
    """
    Broadcasts messages to all connected clients.
    """

    @classmethod
    def filter(cls, web_socket_instance, msg):
        for _id, user in web_socket_instance.users.items():
            if _id != web_socket_instance.id:
                user.sendMessage(msg)
