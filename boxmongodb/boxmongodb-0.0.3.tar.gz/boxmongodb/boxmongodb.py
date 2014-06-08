#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  boxmongodb.py
#  
#  Copyright 2013 Ccdjh <ccdjh.marx@gmail.com>
#  
#
import time
import json
import random

import pymongo

from bson.objectid import ObjectId
from bson import json_util


class Model():
    def __init__(self,**arg):
        class_l   = [val for val in dir(self) if val not in dir(Model)] #减法，去掉model 和self的相同，留下model的Property()值
        if 'BOXURL' in class_l:
            class_l.remove('BOXURL')

        class_list = []
        for i in class_l:
            if i[0:11] =='boxmongodb_':
                pass
            else:
                class_list.append(i)

        class_dict_more = self.__class__.__dict__  #直接在 Property 的返回列表 [me,property_dict,default,{}]

        if class_dict_more.has_key('BOXURL'):
            pymongo_connection = class_dict_more['BOXURL']
        else:
            pymongo_connection = "mongodb://127.0.0.1:27017"

        self.datetime_property = []

        class_dict      = {}
        for li in class_list:
            class_dict[li] = class_dict_more[li] #这个是完整的字典

            if class_dict_more[li][0] == 'datetime_property':
                if class_dict_more[li][1]['auto_now']:
                    self.datetime_property.append((li,class_dict_more[li])) #添加 datetime_property 的功能

        arg_1 = arg
        for class_dict_items in class_dict.items():
            arg_1_has_key = arg_1.has_key(class_dict_items[0])
            if arg_1_has_key:
                arg_1[class_dict_items[0]] = ModelFilter(arg[class_dict_items[0]],class_dict_items[1])#这里对输入值进行过滤
            else:
                arg_1[class_dict_items[0]] = class_dict_items[1][2] #,返回model里面的默认值#首先是外属性0，然后是内属性1，再是默认值2，再是附加值3
        self.pymongo_connection = pymongo_connection
        self.value = arg_1#这个是重点

    @property
    def mongodb_db(self):
        all_name = self.__class__.__name__
        name_list = all_name.split('_')
        db = name_list[0]
        return db

    @property
    def mongodb_table(self):
        all_name = self.__class__.__name__
        name_list = all_name.split('_')
        table = name_list[1]
        return table

    def insert(self):
        all_name = self.__class__.__name__
        name_list = all_name.split('_')
        db = name_list[0]
        table = name_list[1]
        
        self.conn = pymongo.MongoClient(self.pymongo_connection)
        self.db_name = self.conn[db]
        self.db_name_table_name = self.db_name[table]
        data = self.db_name_table_name.insert(self.value) #奇怪的现象是 self.value 被改变了，会被添加ObjectId
        
        return self.value



    @classmethod
    def insert_dict(cls,dic):
        all_name = cls.__name__
        name_list = all_name.split('_')
        db = name_list[0]
        table = name_list[1]
        
        class_dict_more = cls.__dict__
        if class_dict_more.has_key('BOXURL'):
            pymongo_connection = class_dict_more['BOXURL']
        else:
            pymongo_connection = "mongodb://127.0.0.1:27017"
        conn = pymongo.MongoClient(pymongo_connection)
        db_name = conn[db]
        db_name_table_name = db_name[table]
        data = db_name_table_name.insert(dic)
        
        return dic


#删除记录 (不带条件表示全部删除)
#account.remove({"name": "mike"})
    @classmethod
    def remove(cls,name,value):#自己的num或者key
        all_name = cls.__name__
        name_list = all_name.split('_')
        db = name_list[0]
        table = name_list[1]
        
        class_dict_more = cls.__dict__
        if class_dict_more.has_key('BOXURL'):
            pymongo_connection = class_dict_more['BOXURL']
        else:
            pymongo_connection = "mongodb://127.0.0.1:27017"
        conn = pymongo.MongoClient(pymongo_connection)
        db_name = conn[db]
        db_name_table_name = db_name[table]
        data = db_name_table_name.remove({name:value})
        
        return data#应该没有返回值
        

    @classmethod
    def remove_id(cls,value):#只接受id
        all_name = cls.__name__
        name_list = all_name.split('_')
        db = name_list[0]
        table = name_list[1]
        
        class_dict_more = cls.__dict__
        if class_dict_more.has_key('BOXURL'):
            pymongo_connection = class_dict_more['BOXURL']
        else:
            pymongo_connection = "mongodb://127.0.0.1:27017"
        conn = pymongo.MongoClient(pymongo_connection)
        db_name = conn[db]
        db_name_table_name = db_name[table]
        data = db_name_table_name.remove({"_id":ObjectId(value)})
        return data#应该没有返回值

    @classmethod
    def remove_all(cls):#整张表
        all_name = cls.__name__
        name_list = all_name.split('_')
        db = name_list[0]
        table = name_list[1]
        
        class_dict_more = cls.__dict__
        if class_dict_more.has_key('BOXURL'):
            pymongo_connection = class_dict_more['BOXURL']
        else:
            pymongo_connection = "mongodb://127.0.0.1:27017"
        conn = pymongo.MongoClient(pymongo_connection)
        db_name = conn[db]
        db_name_table_name = db_name[table]
        data = db_name_table_name.remove()
        return data#应该没有返回值



    @classmethod
    def find(cls,name,value):#返回值为 对象
        all_name = cls.__name__
        name_list = all_name.split('_')
        db = name_list[0]
        table = name_list[1]
        
        class_dict_more = cls.__dict__
        if class_dict_more.has_key('BOXURL'):
            pymongo_connection = class_dict_more['BOXURL']
        else:
            pymongo_connection = "mongodb://127.0.0.1:27017"
        conn = pymongo.MongoClient(pymongo_connection)
        db_name = conn[db]
        db_name_table_name = db_name[table]
        data = db_name_table_name.find({name:value})
        data = [i for i in data]
        
        return json.dumps(data, sort_keys=True, indent=4, default=json_util.default)
        #返回值为json

    @classmethod
    def find_id(cls,value): #返回值为None#未整理好
        all_name = cls.__name__
        name_list = all_name.split('_')
        db = name_list[0]
        table = name_list[1]

        class_dict_more = cls.__dict__
        if class_dict_more.has_key('BOXURL'):
            pymongo_connection = class_dict_more['BOXURL']
        else:
            pymongo_connection = "mongodb://127.0.0.1:27017"
        conn = pymongo.MongoClient(pymongo_connection)
        db_name = conn[db]
        db_name_table_name = db_name[table]
        data = db_name_table_name.find_one({"_id":ObjectId(value)})
        #data = [i for i in data]
        return json.dumps(data, sort_keys=True, indent=4, default=json_util.default)
        #返回值为json

    @classmethod
    def find_all(cls):
        all_name = cls.__name__
        name_list = all_name.split('_')
        db = name_list[0]
        table = name_list[1]
        
        class_dict_more = cls.__dict__
        if class_dict_more.has_key('BOXURL'):
            pymongo_connection = class_dict_more['BOXURL']
        else:
            pymongo_connection = "mongodb://127.0.0.1:27017"
        conn = pymongo.MongoClient(pymongo_connection)
        db_name = conn[db]
        db_name_table_name = db_name[table]
        data = db_name_table_name.find()
        data = [i for i in data]
        return json.dumps(data, sort_keys=True, indent=4, default=json_util.default)
        #返回值为json

    def update(self,name,value):
        all_name = self.__class__.__name__
        name_list = all_name.split('_')
        db = name_list[0]
        table = name_list[1]
        
        #self.datetime_property
        
        self.conn = pymongo.MongoClient(self.pymongo_connection)
        self.db_name = self.conn[db]
        self.db_name_table_name = self.db_name[table]


        data_old = self.db_name_table_name.find({name:value})
        data_old = [i for i in data_old]

        new_value = {}
        new_value.update(self.value)

        if len(data_old) == 0:
            pass
        else:
            for i in self.datetime_property:
                    new_value[i[0]] = data_old[0][i[0]]

        data = self.db_name_table_name.update({name:value},{"$set":new_value})
        return data#返回ture 布尔值

    def update_id(self,value):
        all_name = self.__class__.__name__
        name_list = all_name.split('_')
        db = name_list[0]
        table = name_list[1]
        
        self.conn = pymongo.MongoClient(self.pymongo_connection)
        self.db_name = self.conn[db]
        self.db_name_table_name = self.db_name[table]

        data_old = self.db_name_table_name.find_one({"_id":ObjectId(value)})

        new_value = {}
        new_value.update(self.value)

        if len(data_old) == 0:
            pass
        else:
            for i in self.datetime_property:
                    new_value[i[0]] = data_old[i[0]]

        data = self.db_name_table_name.update({"_id":ObjectId(value)},{"$set":new_value})
        return data#返回ture 布尔值

    @classmethod
    def update_id_dict(cls,value,dic):
        all_name = cls.__name__
        name_list = all_name.split('_')
        db = name_list[0]
        table = name_list[1]
        
        class_dict_more = cls.__dict__
        if class_dict_more.has_key('BOXURL'):
            pymongo_connection = class_dict_more['BOXURL']
        else:
            pymongo_connection = "mongodb://127.0.0.1:27017"
        conn = pymongo.MongoClient(pymongo_connection)
        db_name = conn[db]
        db_name_table_name = db_name[table]
        data = db_name_table_name.update({"_id":ObjectId(value)},{"$set":dic},multi=True)

class ModelFilter(object):#有长度
    def __new__(cls,value,v2):
        if v2[0] == 'string_property':
            return value #过滤是否合格的字符串
        if v2[0] == 'datetime_property':
            return value #过滤是否合格的DateTime格式
        if v2[0] == 'integer_property':
            return value #过滤是否合格的Integer格式
        if v2[0] == 'link_property':
            return value #过滤是否合格的link格式
        if v2[0] == 'auth_property':
            return value #过滤是否合格的auth格式
        if v2[0] == 'dict_property':
            return value #过滤是否合格的dict格式
        if v2[0] == 'email_property':
            return value #过滤是否合格的dict格式

#首先是外属性，然后是内属性，再是默认值，再是附加值
class StringProperty(object):
    def __new__(cls,**arg):
        string_property_arg = arg
        me = 'string_property'
        string_property_dict ={}
        default_io = string_property_arg.has_key('default')
        default  = string_property_arg['default'] if default_io else None
        return [me,string_property_dict,default,{}]


class DateTimeProperty(object):
    def __new__(cls,**arg):
        datetime_property_arg = arg
        me = 'datetime_property'

        default_io = datetime_property_arg.has_key('default')
        default = datetime_property_arg['default'] if default_io else str(int(time.time()))

        #default = str(int(time.time()))
        auto_now_add_io = datetime_property_arg.has_key('auto_now_add')
        auto_now_io     = datetime_property_arg.has_key('auto_now')
        datetime_property_dict = {}#后期启用这功能
        datetime_property_dict['auto_now_add']  = datetime_property_arg['auto_now_add'] if auto_now_add_io else None
        datetime_property_dict['auto_now']      = datetime_property_arg['auto_now'] if auto_now_io else None
        return [me,datetime_property_dict,default,{}]

class IntegerProperty(object):#纯数字
    def __new__(cls,**arg):
        integer_property_arg = arg
        me = 'integer_property'

        default_io = integer_property_arg.has_key('default')
        default = integer_property_arg['default'] if default_io else str(0)
        integer_property_dict = {}
        return [me,integer_property_dict,default,{}]

class LinkProperty(object):
    def __new__(cls,**arg):
        link_property_arg = arg
        me = 'link_property'

        default_io = link_property_arg.has_key('default')
        default = link_property_arg['default'] if default_io else None
        link_property_dict = {}
        return [me,link_property_dict,default,{}]

class AuthProperty(object):
    def __new__(cls,**arg):
        auth_property_arg = arg
        me = 'auth_property'

        t = str(int(time.time()))
        ex = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
        e = "".join(random.sample(ex,10))
        x = "".join(random.sample(ex,10))

        default_io = auth_property_arg.has_key('default')
        default = auth_property_arg['default'] if default_io else t + e + x
        auth_property_dict = {}
        return [me,auth_property_dict,default,{}]

class DictProperty(object):
    def __new__(cls,**arg):
        dict_property_arg = arg
        me = 'dict_property'

        default_io = dict_property_arg.has_key('default')
        default = dict_property_arg['default'] if default_io else {}
        dict_property_dict = {}
        return [me,dict_property_dict,default,{}]

class EmailProperty(object):
    def __new__(cls,**arg):
        email_property_arg = arg
        me = 'email_property'

        default_io = email_property_arg.has_key('default')
        default = email_property_arg['default'] if default_io else None
        email_property_dict = {}
        return [me,email_property_dict,default,{}]


