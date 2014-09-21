#coding: utf-8

from django.contrib import messages


class DBMessageMiddleware(object):
    """
    Uses ``django.contrib.messages`` to add to the request any messages that
    authenticated user might have stored for them,
    and marks those messages as read.
    """

    def process_request(self, request):
        if not request.user.is_authenticated():
            return

        user_messages = request.user.dbmessages.all()

        if len(user_messages) < 1:
            return

        for msg in user_messages:
            messages.add_message(request, msg.level, msg.message, msg.extra_tags)

        user_messages.delete()
