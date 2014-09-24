#coding:utf-8
'''
Created on 04.01.2011

@author: kirov
'''
import random

from django.test import TestCase

from palo_olap.server import PaloServer
from palo_olap.dimension import ELEMENT_TYPE_CONSOLIDATED, ELEMENT_TYPE_STRING, ELEMENT_TYPE_NUMERIC

DB_NAME = 'olap_test'
YEAR_DIM = u'Года'
MON_DIM = u'Месяцы'
MONTH_NAMES = (
        (1,u'Январь'),
        (2,u'Февраль'),
        (3,u'Март'),
        (4,u'Апрель'),
        (5,u'Май'),
        (6,u'Июнь'),
        (7,u'Июль'),
        (8,u'Август'),
        (9,u'Сентябрь'),
        (10,u'Октябрь'),
        (11,u'Ноябрь'),
        (12,u'Декабрь'),
    )
UNIT_DIM = u'Учреждения'
MAX_UNITS = 50000

class PaloTests(TestCase):
    '''
    Тесты Palo Olap
    '''
    def test_1(self):
        p = PaloServer(server_host='localhost',user='admin',password='admin')
        # подключаемся к серверу
        p.login()
        # загружаем список баз
        p.load_db_list()
        # проверяем наличие базы 'olap_test'
        if p.db_exists(DB_NAME):
            # получаем базу
            db = p.get_db(DB_NAME)
        else:
            # создаем базу
            db = p.create_db(DB_NAME)
        
        #db.load_dimensions()
        # проверим в базе наличие размерности 'years'
        if db.dimension_exists(YEAR_DIM):
            d_years = db.get_dimension(YEAR_DIM)
        else:
            d_years = db.create_dimension(YEAR_DIM)
        
        # очистим размерность
        d_years.clear()
        # заполним ее годами
        years_list = []
        for year in range(2000,2010+1):
            res = d_years.create_element(u'%s год' % year)
            years_list.append(u'%s год' % year) # тут имя элемента
        d_years.create_consolidate_element(u'Все года', years_list)
        
        # тоже сделаем и с месяцами
        if db.dimension_exists(MON_DIM):
            d_mons = db.get_dimension(MON_DIM)
        else:
            d_mons = db.create_dimension(MON_DIM)
        d_mons.clear()
        month_list = []
        for month in range(1,12+1):
            res = d_mons.create_element(MONTH_NAMES[month-1][1])
            month_list.append(MONTH_NAMES[month-1][1])
        d_mons.create_consolidate_element(u'Все месяцы', month_list)
        
        # попробуем добавить большое количество учреждений
        if db.dimension_exists(UNIT_DIM):
            d_units = db.get_dimension(UNIT_DIM)
        else:
            d_units = db.create_dimension(UNIT_DIM)
        d_units.clear()
        unit_list = []
        for unit in range(1,MAX_UNITS/10+1):
            res = d_units.create_element(u'Учреждение №%s' % unit)
            unit_list.append(u'Учреждение №%s' % unit)
        all_units_id = d_units.create_consolidate_element(u'Все учреждения', unit_list)
        
        # дополним еще большим количеством учреждений
        unit_list = []
        unit_id_list = []
        for unit in range(MAX_UNITS/10+1,MAX_UNITS+1):
            unit_list.append(u'Учреждение №%s' % unit)
            # id будет совпадать с номером учреждения, поэтому пока не загоняемся
            unit_id_list.append(unit)
        d_units.create_elements(unit_list)
        # добавим новые учреждения во "Все учреждения"
        d_units.append_to_consolidate_element(all_units_id, unit_id_list)
        
        # создадим промежуточные группировочные элементы
        g_ids = []
        for g_unit in range(1, 10+1):
            id_list = []
            if g_unit == 1:
                for unit in range(0, MAX_UNITS/10):
                    id_list.append((g_unit-1)*MAX_UNITS/10+unit)
            else:
                for unit in range(1, MAX_UNITS/10+1):
                    id_list.append((g_unit-1)*MAX_UNITS/10+unit)
            g_id = d_units.create_element(u'Группа %s' % g_unit, ELEMENT_TYPE_CONSOLIDATED, id_list)
            g_ids.append(g_id)
            d_units.append_to_consolidate_element(all_units_id, [g_id])
        
        # оставим во "Все учреждения" только группы
        d_units.replace_consolidate_element(all_units_id, g_ids)
        
        # сохраним базу
        db.save()
        
        db.load_cubes()
        # проверим что есть куб или создадим новый
        if db.cube_exists(u'Численность'):
            c_count = db.get_cube(u'Численность')
        else:
            dims = [d_years.get_id(), d_mons.get_id(), d_units.get_id()]
            #без разреза учреждений
            #dims = [d_years.get_id(), d_mons.get_id()]
            c_count = db.create_cube(u'Численность', dims)
        
        # очистим куб
        c_count.clear(('*','*','*'))
        
        # заполним куб какими-то значениями
        #coord = (u'2005 год', u'Декабрь')
        coord = (u'2005 год', u'Декабрь', u'Учреждение №130')
        c_count.replace(coord, 1)
        #coord = (u'2002 год', u'Январь')
        coord = (u'2005 год', u'Декабрь', u'Учреждение №349')
        c_count.replace(coord, 23.45)
        
        # заполним массово
        coords = []
        values = []
        for counter in range(1, 100000+1):
            # случайно выберем год
            year = random.randint(2000,2010)
            year_name = u'%s год' % year
            #year_id = d_years.getElementID(year_name)
            
            # выберем месяц
            month = random.randint(1,12)
            mon_name = MONTH_NAMES[month-1][1]
            #mon_id = d_mons.getElementID(mon_name)
            
            # выберем учреждение
            unit = random.randint(1, MAX_UNITS)
            unit_name = u'Учреждение №%s' % unit
            #unit_id = d_units.getElementID(unit_name)
            
            # случайное значение
            value = round(random.random()*100)
            
            coords.append((year_name, mon_name, unit_name))
            values.append(value)
            
        cres = c_count.replace_bulk(coords, values)
        
        # сохраним базу
        db.save()