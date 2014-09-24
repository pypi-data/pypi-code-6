#coding:utf-8
'''
Created on 07.12.2010

@author: akvarats
'''

from m3.ui import actions

class TestActionPack1(actions.ActionPack):
    '''
    '''
    url = '/pack1'
    
    
    def __init__(self):
        super(TestActionPack1, self).__init__()
        self.actions.extend([TestAction11(), 
                             TestAction12, 
                             'tests.helpers.urls_tests.actions.TestAction13',])
    
class TestActionPack2(actions.ActionPack):
    '''
    '''
    url = '/pack2'
    
    def __init__(self):
        super(TestActionPack2, self).__init__()
        self.shortname = 'test-action-12'
        self.actions.extend([TestAction21, 
                             TestAction22(),
                             'tests.helpers.urls_tests.actions.TestAction23',])
    
    
class TestAction11(actions.Action):
    '''
    '''
    url = '/action1'
    shortname = 'test-action-11'
    
    
class TestAction12(actions.Action):
    '''
    '''
    url = '/action2'
    short_name = 'test-action-12'
    
class TestAction13(actions.Action):
    '''
    '''
    url = '/action3'
     


class TestAction21(actions.Action):
    '''
    '''
    url = '/action1'
    def __init__(self):
        super(TestAction21, self).__init__()
        self.shortname = 'test-action-21'
    
class TestAction22(actions.Action):
    '''
    '''
    url = '/action2'
    
    def __init__(self):
        super(TestAction22, self).__init__()
        self.shortname = 'test-action-22'
    
class TestAction23(actions.Action):
    '''
    '''
    url = '/action3'