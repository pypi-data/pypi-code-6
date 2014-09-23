#coding:utf-8
'''
Created on 18.11.11
@author: akvarats
'''

from m3.ui import actions
from m3.ui.actions import async

from background import  BackgroundLoader

class ActionsTestsPack(actions.ActionPack):
    '''
    '''
    url = '/actions'
    shortname = 'actions-tests-pack'

    def __init__(self):
        super(ActionsTestsPack, self).__init__()
        self.actions.extend([AliveAction(),
                             BackgroundAction(),])

class AliveAction(actions.Action):
    '''
    Действие, которое выполняет захват семафора с очень которотким таймаутом
    '''

    url = '/alive'
    shortname = 'actions-tests.alive'

    def run(self, request, context):
        '''
        '''
        return actions.TextResult('ok')

class BackgroundAction(async.AsyncAction):

    url = '/background'
    shortname = 'actions-tests.background'
    worker_cls = BackgroundLoader
