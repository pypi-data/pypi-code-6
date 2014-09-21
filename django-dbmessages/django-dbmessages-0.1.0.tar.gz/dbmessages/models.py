#coding: utf-8

import django
from django.conf import settings
from django.db import models
from django.contrib.messages.storage.base import Message as stock_message_cls


def get_user_model_fk_ref():
    ver = django.VERSION

    if ver[0] >= 1 and ver[1] >= 5:
        return settings.AUTH_USER_MODEL
    else:
        return 'auth.User'


class Message(models.Model):
    to_user = models.ForeignKey(get_user_model_fk_ref(),
        related_name='dbmessages')

    level = models.IntegerField(help_text=
        "A number. The values for the built-in levels are:"
        "<table>"
        "<tr><th>Level Constant<th>Value"
        "<tr><td>DEBUG   <td>10"
        "<tr><td>INFO    <td>20"
        "<tr><td>SUCCESS <td>25"
        "<tr><td>WARNING <td>30"
        "<tr><td>ERROR   <td>40"
        "</table>")

    message = models.TextField(default="")

    extra_tags = models.TextField(default="", blank=True, help_text=
        "Space-separated words.")

    @property
    def message_compat(self):
        return stock_message_cls(self.level, self.message, self.extra_tags)

    def __unicode__(self):
        return unicode(self.message_compat)
