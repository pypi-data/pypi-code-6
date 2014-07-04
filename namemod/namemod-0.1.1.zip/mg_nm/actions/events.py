'''
Created on 01/06/2014

@author: Ronaldo Webb
'''

import abc

class AbstractEvent(metaclass=abc.ABCMeta):
    '''
    The base class of all the Events available 
    '''
    
    @abc.abstractmethod
    def data(self):
        '''
        The event that must be implemented by the subclass.
        '''
        pass

class ActionEvent(AbstractEvent):
    '''
    The event dedicated to the subclasses of mg_nm.actions.AbstractAction.
    '''
    
    def __init__(self, **kwargs):
        self.args = kwargs

    def data(self): 
        return self.args
    
