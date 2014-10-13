from django.utils.translation import ugettext as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool



from .models import TabUi, TabUiList

class TabUiListPlugin(CMSPluginBase):
    model = TabUiList
    name = _('Tab list group')
    render_template = 'cmsplugin_tab_ui/tablist.html'
    allow_children = True
    child_classes = ['TabUiPlugin']
    
    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
        })
        return context

class TabUiPlugin(CMSPluginBase):
    model = TabUi
    name = _('Tab Field')
    render_template = 'cmsplugin_tab_ui/tabfield.html'
    allow_children = True 
    #child_classes = ['CMSPluginBase']
    parent_classes = ['TabUiListPlugin']
    
    def render(self, context, instance, placeholder):
        context.update({
                'instance': instance,
                'placeholder':placeholder,
                })
        return context  
    
plugin_pool.register_plugin(TabUiListPlugin)
plugin_pool.register_plugin(TabUiPlugin)