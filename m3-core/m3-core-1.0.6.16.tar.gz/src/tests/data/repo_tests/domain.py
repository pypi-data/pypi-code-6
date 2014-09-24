#coding:utf-8
'''
Created on 28.07.2011

@author: akvarats
'''

class Contragent(object):
    '''
    '''
    def __init__(self):
        self.code = ''
        self.name = ''
        self.comment = ''
        
    def attributes(self):
        return ['code',
                'name',
                'comment',]
    
    
class LPU(object):
    '''
    '''
    def __init__(self):
        self.contragent = None
        self.chieff = ''
        self.comment = ''
        
    def attributes(self):
        return ['chieff', 
                'comment',]
        