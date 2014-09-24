# -*- coding: utf-8 -*-

import objectpack
from m3_ext.ui import all_components as ext


class MsgWindow(objectpack.BaseWindow):

    def _init_components(self):
        self.out = ext.ExtTextArea(read_only=True)
        self.inp = ext.ExtStringField()
        self.btn = ext.ExtButton(text='Отправить')

    def _do_layout(self):
        self.layout = 'border'

        input_ctr = ext.ExtContainer(layout='fit', flex=1)
        input_ctr.items.append(self.inp)

        bottom_panel = ext.ExtContainer(
            layout='hbox', height=22, region='south')
        bottom_panel.items.extend((input_ctr, self.btn))

        self.out.region = 'center'
        self.items.extend((self.out, bottom_panel))

    def set_params(self, params):
        super(MsgWindow, self).set_params(params)
        self.template_globals = 'msgwindow.js'
        self.send_url = params['send_url']
        self.btn.handler = 'sendMessage'
