__author__ = 'The NetYeti'


from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from .models import ServerStatus, ServerQuery, PluginsList


class MinecraftServerStatusPlugin(CMSPluginBase):
    model = ServerStatus
    render_template = "minecraft/server_status.html"
    name = _("Server Status")
    module = "Minecraft"
    admin_preview = True
    text_enabled = True
    cache = True

    def render(self, context, instance, placeholder):

        from djangocms_minecraft.query import MinecraftQuery

        mchost = instance.mchost
        mcport = instance.mcport

        try:
            query = MinecraftQuery(host=mchost, port=mcport)
        except Exception as e:
            print e
            # Need to do something here?
        else:
            context['status'] = query.get_status()
            context['instance'] = instance

        return context

plugin_pool.register_plugin(MinecraftServerStatusPlugin)


class MinecraftServerQueryPlugin(CMSPluginBase):
    model = ServerQuery
    render_template = "minecraft/server_query.html"
    name = _("Server Query")
    module = "Minecraft"
    admin_preview = True
    text_enabled = True
    cache = True

    def render(self, context, instance, placeholder):

        from djangocms_minecraft.query import MinecraftQuery

        mchost = instance.mchost
        mcport = instance.mcport

        try:
            query = MinecraftQuery(host=mchost, port=mcport)
        except Exception as e:
            pass
            # Need to do something here?
        else:
            context['status'] = query.get_rules()
            context['instance'] = instance

        return context

plugin_pool.register_plugin(MinecraftServerQueryPlugin)


class MinecraftPluginsListPlugin(CMSPluginBase):
    model = PluginsList
    render_template = "minecraft/plugins_list.html"
    name = _("Installed Plugins")
    module = "Minecraft"
    admin_preview = True
    text_enabled = True
    cache = True

    def render(self, context, instance, placeholder):

        from djangocms_minecraft.query import MinecraftQuery

        mchost = instance.mchost
        mcport = instance.mcport

        try:
            query = MinecraftQuery(host=mchost, port=mcport)
        except Exception as e:
            pass
            # Need to do something here?
        else:
            context['plugins'] = query.get_rules()['plugins']
            context['instance'] = instance

        return context

plugin_pool.register_plugin(MinecraftPluginsListPlugin)

