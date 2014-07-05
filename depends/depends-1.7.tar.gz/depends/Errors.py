'''
Created on Jun 18, 2014

@author: francis
'''

class DependsError(Exception):
    pass

class CircularDependencyError(DependsError):
    def __init__(self, v):
        v = '%s'%v
        super(Exception, self).__init__(v)
        self.chain = [v]
    def __str__(self):
        return 'CIRC(%s)'%'.'.join(self.chain)

class InvalidDependantName(DependsError):
    def __str__(self):
        return 'InvalidDependantName(%s)'%self.message

