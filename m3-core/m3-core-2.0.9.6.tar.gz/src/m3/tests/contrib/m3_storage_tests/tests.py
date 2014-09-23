#coding:utf-8
'''
Created on 13.05.2011

@author: akvarats
'''

from django.test import TestCase
from django.db import connections


from m3_storage.models import (StorageConfigurationModel,
                                          StorageTableModel,
                                          TableFieldModel,
                                          TableRelationModel,
                                          FieldTypeEnum,
                                          RelationTypeEnum,)

from m3_storage.api import activate_configuration

class StorageTests(TestCase):
    '''
    Тесты для подсистемы m3_storage
    '''
    
    def test_configuration_1(self):
        
        cfg_1 = self.create_configuration_1()
        
        # здесь должны создасться таблицы table1 и table2 с соответствующим
        # набором полей
        activate_configuration(cfg_1)
        
        
        cursor = connections['default'].cursor()
        cursor.execute('SELECT count(char1) FROM table1')
        for row in cursor:
            self.assertEqual(row[0], 0)
            
        cursor.execute('SELECT count(char2) FROM table1')
        for row in cursor:
            self.assertEqual(row[0], 0)
            
        cursor.execute('SELECT count(char1) FROM table2')
        for row in cursor:
            self.assertEqual(row[0], 0)
            
        cursor.execute('SELECT count(char2) FROM table2')
        for row in cursor:
            self.assertEqual(row[0], 0)
    
    
    
    #===========================================================================
    # Хелперные методы
    #===========================================================================
    def create_configuration_1(self):
        '''
        Метод создает начальную конфигурацию
        '''
        
        cfg = StorageConfigurationModel()
        cfg.version = 1
        cfg.save()
        
        # создаем таблицы в данной конфигурации
        
        table1 = StorageTableModel.objects.create(name='table2',
                                                  configuration=cfg)
        
        TableFieldModel.objects.create(table=table1,
                                       name='char1',
                                       type=FieldTypeEnum.CHAR,
                                       size = 200,
                                       allow_blank = True)
        
        TableFieldModel.objects.create(table=table1,
                                       name='char2',
                                       type=FieldTypeEnum.CHAR,
                                       size = 200,
                                       allow_blank = True)

        
        table2 = StorageTableModel.objects.create(name='table2',
                                                  configuration=cfg)
        
        TableFieldModel.objects.create(table=table2,
                                       name='char1',
                                       type=FieldTypeEnum.CHAR,
                                       size = 200,
                                       allow_blank = True)
        
        TableFieldModel.objects.create(table=table2,
                                       name='char2',
                                       type=FieldTypeEnum.CHAR,
                                       size = 200,
                                       allow_blank = True)
        
        return cfg