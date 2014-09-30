# coding: utf-8

from m3_ext.demo.actions.base import Pack, UIAction
from m3_ext.ui import all_components as ext

from kladr.addrfield import ExtAddrComponent

@Pack.register
class KladrFieldAction(UIAction):
    """
    Пример окна с полем адреса КЛАДР.
    """
    title = u'КЛАДР'

    def get_ui(self, request, context):
        win = ext.ExtWindow(
            layout=ext.ExtForm.FIT,
            width=400,
            height=400,
            maximizable=False,
            minimizable=False,
            buttons=[
                ext.ExtButton(text=u'Закрыть')
            ],
            items=[
                ExtAddrComponent()
            ])

        return win
