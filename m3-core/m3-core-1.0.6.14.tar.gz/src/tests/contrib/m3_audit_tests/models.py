#coding:utf-8
'''
Created on 22.12.2010

@author: akvarats
'''

from m3_audit import BaseAuditModel, AuditManager


class MyAuditModel(BaseAuditModel):
    
    @staticmethod
    def write(user):
        pass
    
    class Meta:
        db_table = 'myaudit_model'
        
        
AuditManager().register('my-audit', MyAuditModel)