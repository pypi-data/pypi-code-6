#coding:utf-8
'''
Created on 27.04.2011

@author: akvarats
'''

from django.test import TestCase
from django.db import connections

from m3.db import ddl

from migrator import SimpleMigrator
from django.db.utils import DatabaseError

class DiffTests(TestCase):
    
    def test_exceptions(self):
        '''
        В ходе теста проверяем выдачу исключительных ситуаций на случаи когда
        в метод миграции передаются некорректные пары левой и правой таблиц.
        '''
        migrator = ddl.BaseMigrator()
        
        left_table = ddl.DBTable('my_table')
        right_table = ddl.DBTable('my_table')
        another_table = ddl.DBTable('another_table')
        
        # во всех указанных ниже комбинациях параметров методы должны громко падать
        self.assertRaises(Exception, migrator.migrate, to_version=None)
        self.assertRaises(Exception, migrator.migrate, to_version=ddl.NullTable)
        self.assertRaises(Exception, migrator.migrate, to_version=ddl.NullTable, from_version=ddl.NullTable)
        
        self.assertRaises(Exception, migrator.migrate, to_version=None, from_version=left_table)
        self.assertRaises(Exception, migrator.migrate, to_version=left_table, from_version=another_table)
        self.assertRaises(Exception, migrator.migrate, to_version=another_table, from_version=right_table)
        #self.assertRaises(Exception, migrator.migrate, to_version=left_table, from_version=right_table)
        
    def test_create_drop_table(self):
        '''
        Проверяем как выполняется создание таблиц
        '''
        right_table = ddl.DBTable('my_table')
        right_table.fields.append(ddl.IDField())
        right_table.fields.append(ddl.CharField(name='name_field', max_length=200))
        
        migrator = SimpleMigrator()
        migrator.migrate(from_version=ddl.NullTable(),
                         to_version=right_table,)       
        
        cursor = connections['default'].cursor()
        cursor.execute('SELECT count(name_field) FROM my_table')
        for row in cursor:
            self.assertEqual(row[0], 0)
            
            
        migrator.migrate(from_version=right_table,
                         to_version=ddl.NullTable(),)
            
        cursor = connections['default'].cursor()
        self.assertRaises(DatabaseError, cursor.execute, 'SELECT count(name_field) FROM my_table')
        
    def test_append_field(self):
        
        table1 = ddl.DBTable('my_table')
        table1.fields.append(ddl.IDField())
        table1.fields.append(ddl.CharField(name='name_field', max_length=200))
        
        table2 = ddl.DBTable('my_table')
        table2.fields.append(ddl.IDField())
        table2.fields.append(ddl.CharField(name='name_field', max_length=200))
        table2.fields.append(ddl.CharField(name='xyz_field', max_length=200))
        
        migrator = SimpleMigrator()
        migrator.migrate(from_version=ddl.NullTable(),
                         to_version=table1,)
        
        migrator.migrate(from_version=table1,
                         to_version=table2,)
        
        cursor = connections['default'].cursor()
        cursor.execute('SELECT count(xyz_field) FROM my_table')
        for row in cursor:
            self.assertEqual(row[0], 0)
            
        migrator.migrate(from_version=table2, to_version=ddl.NullTable())
        
    def test_create_fields(self):
        '''
        '''
        
        table = ddl.DBTable('my_table_333')
        table.fields.append(ddl.IDField())
        table.fields.append(ddl.CharField(name='char1', max_length=200, allow_blank=False, indexed=False))
        table.fields.append(ddl.CharField(name='char2', max_length=200, allow_blank=True, indexed=False))
        table.fields.append(ddl.CharField(name='char3', max_length=200, allow_blank=False, indexed=True))
        table.fields.append(ddl.CharField(name='char4', max_length=200, allow_blank=True, indexed=True))
        
        table.fields.append(ddl.DateField(name='date1'))
        table.fields.append(ddl.DateTimeField(name='datetime1'))
        
        table.fields.append(ddl.TextField(name='text1'))
        
        table.fields.append(ddl.IntegerField(name='int1'))
        table.fields.append(ddl.DecimalField(name='decimal1'))
        
        migrator = SimpleMigrator()
        migrator.create_table(table)
        
        
        cursor = connections['default'].cursor()
        cursor.execute('SELECT id, char1, char2, char3, char4, date1, datetime1, text1, int1, decimal1 FROM %s' % table.name)
        for row in cursor:
            pass
        
        migrator.drop_table(table)