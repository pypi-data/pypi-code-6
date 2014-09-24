# -*- coding: utf-8 -*-

import objectpack
from m3 import actions as m3_actions

from pushme.mq import get_sender

import ui


class Pack(objectpack.BasePack):

    title = u'PushMe'

    add_to_desktop = True

    def __init__(self):
        super(Pack, self).__init__()
        self.window_action = WindowAction()
        self.send_actiion = SendAction()
        self.actions.extend((
            self.window_action,
            self.send_actiion,
        ))

    def get_default_action(self):
       return self.window_action


class WindowAction(objectpack.BaseWindowAction):
    def create_window(self):
        self.win = ui.MsgWindow()

    def set_window_params(self):
        self.win_params['title'] = self.parent.title
        self.win_params['send_url'] = (
            self.parent.send_actiion.get_absolute_url()
        )


class SendAction(objectpack.BaseAction):
    def run(self, request, context):
        msg = request.REQUEST.get('message')

        sender = get_sender('snakemq', ('localhost', 4000))
        sender.send(topic='echo', data=msg)

        return m3_actions.OperationResult(success=True)
