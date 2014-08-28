__author__ = 'growlf'

from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _

class MinecraftServer(CMSPlugin):
    name = models.CharField(_('Name'), help_text='Host name or server alias to use in the title of this plugin output',
                            max_length=50)
    mchost = models.GenericIPAddressField(_('Minecraft Host'),
                                          help_text='IP address or hostname to access the Minecraft server via',
                                          default='127.0.0.1')
    mcport = models.PositiveIntegerField(_('Query Port'),
                                         help_text='Port to use for ping and query protocols.  Typically this is 25565 '
                                                   '(same as the Minecraft client connection port).', default=25565)
    rconport = models.PositiveIntegerField(_('RCON Port'),
                                           help_text='The port to use for RCON access - not required, and not enabled '
                                                     'by default. (Typical port used for RCON is 25575)', default=25575)
    map_url = models.CharField(_('Map URL'),
                               help_text='The url prefix for map links.  This can include zoom level, map type and more'
                                         ' if you are using something like Dynmap. It can also just be a static prefix'
                                         ' for static page sets where the map-name is appended to the end of the URL.',
                               max_length=80, default="http://www.thenetyeti.com:8123/?mapname=surface&zoom=8")
