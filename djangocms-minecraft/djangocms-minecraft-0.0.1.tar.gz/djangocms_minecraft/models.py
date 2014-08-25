__author__ = 'growlf'

from cms.models.pluginmodel import CMSPlugin
from django.db import models

ZOOM_LEVEL_CHOICES = zip(range(1, 8), range(1, 8))


class ServerStatus(CMSPlugin):
    mchost = models.IPAddressField(default='127.0.0.1')
    mcport = models.PositiveIntegerField(default=25565)


class ServerQuery(CMSPlugin):
    mchost = models.IPAddressField(default='127.0.0.1')
    mcport = models.PositiveIntegerField(default=25565)
    map_url = models.CharField(max_length=80, default="http://www.thenetyeti.com:8123/?mapname=surface&zoom=8")


class PluginsList(CMSPlugin):
    mchost = models.IPAddressField(default='127.0.0.1')
    mcport = models.PositiveIntegerField(default=25565)


# class RCon(CMSPlugin):
#     mchost = models.IPAddressField(default='127.0.0.1')
#     mcport = models.PositiveIntegerField(default=25575)
#     mcpwd = models.CharField(max_length=16)

