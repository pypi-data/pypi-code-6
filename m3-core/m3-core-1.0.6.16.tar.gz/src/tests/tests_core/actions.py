#coding:utf-8
'''
Created on 22.07.2011

@author: akvarats
'''

from m3.ui import actions

class CoreActionPack(actions.ActionPack):
    '''
    
    '''
    url = '/core'
    shortname = 'core-pack'
    
    def __init__(self):
        super(CoreActionPack, self).__init__()
        self.actions.extend([AliveAction(), ])
        
        
class AliveAction(actions.Action):
    '''
    Действие, обращение к которому позволяет понять, работает ли
    тестовый клиент
    '''
    url = '/alive'
    shortname = 'core.alive-action'
    
    def run(self, request, context):
        return actions.TextResult('ok')
    
    
