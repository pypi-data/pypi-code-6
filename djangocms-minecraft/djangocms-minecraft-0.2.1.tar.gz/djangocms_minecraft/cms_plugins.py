__author__ = 'The NetYeti'


from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from .models import MinecraftServer
from djangocms_minecraft.query import MinecraftQuery
import socket


class MinecraftServerStatusPlugin(CMSPluginBase):
    model = MinecraftServer
    render_template = "minecraft/server_status.html"
    name = _("Server Status")
    module = "Minecraft"
    admin_preview = True
    text_enabled = True

    def render(self, context, instance, placeholder):

        mchost = instance.mchost
        mcport = instance.mcport
        status = cache.get(mchost+"_status")

        if not status:

            try:
                query = MinecraftQuery(host=mchost, port=mcport, timeout=5)
                status = query.get_status()
            except socket.error as e:
                status = None
            else:
                cache.set(mchost+"_status", status)

        context.update({
            'status': status,
            'instance': instance,
        })

        return context

plugin_pool.register_plugin(MinecraftServerStatusPlugin)


class MinecraftServerQueryPlugin(CMSPluginBase):
    model = MinecraftServer
    render_template = "minecraft/server_query.html"
    name = _("Server Query")
    module = "Minecraft"
    admin_preview = True
    text_enabled = True

    def render(self, context, instance, placeholder):

        mchost = instance.mchost
        mcport = instance.mcport
        status = cache.get(mchost+"_full")

        if not status:

            try:
                query = MinecraftQuery(host=mchost, port=mcport, timeout=5)
                status = query.get_rules()
            except socket.error as e:
                status = None
            else:
                cache.set(mchost+"_full", status)

        context.update({
            'status': status,
            'instance': instance,
        })

        return context

plugin_pool.register_plugin(MinecraftServerQueryPlugin)


class MinecraftPluginsListPlugin(CMSPluginBase):
    model = MinecraftServer
    render_template = "minecraft/plugins_list.html"
    name = _("Installed Plugins")
    module = "Minecraft"
    admin_preview = True
    text_enabled = True
    cache = True

    def render(self, context, instance, placeholder):

        mchost = instance.mchost
        mcport = instance.mcport
        status = cache.get(mchost+"_full")

        if not status:

            try:
                query = MinecraftQuery(host=mchost, port=mcport, timeout=5)
                status = query.get_rules()
            except socket.error as e:
                status = None
            else:
                cache.set(mchost+"_full", status)

        context.update({
            'plugins': status['plugins'],
            'instance': instance,
        })

        return context

plugin_pool.register_plugin(MinecraftPluginsListPlugin)

