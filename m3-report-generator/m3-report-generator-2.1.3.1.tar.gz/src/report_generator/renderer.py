#coding:utf-8
#@author: Excinsky

'''
Пакет для классов, отвечающих за отрисовку конечных клиентских javascript'ов

Перегружает стандартный м3шный рендерер панелей, так как нам нужна поддержка
template_globals
'''
from django.conf import settings


from m3_ext.ui import js
from m3_ext.ui.base import ExtUIScriptRenderer
from m3_ext.ui import render_template


class ExtPanelRenderer(ExtUIScriptRenderer):
    '''
    Рендерер для скрипта на показ панели
    '''
    def __init__(self, component):
        super(ExtPanelRenderer, self).__init__()
        self.component = component

    def get_script(self):
        script = render_template(self.template,
            {'renderer': self, 'component': self.component})
        if settings.DEBUG:
            script = js.JSNormalizer().normalize(script)
        return script