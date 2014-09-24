#coding:utf-8
'''
Created on 11.12.2010

@author: akvarats
'''

from django.db.models.query_utils import Q

def spaced_q_expressions(filter_text, fields):
    '''
    Фильтрация производится по полям списку полей fields и введеному пользователем тексту filter_text.
    Пример:
        fields = ['name', 'family']
        filter_text = u'Вася Пупкин'
    Получится условие WHERE:
        (name like 'Вася' AND name like 'Пупкин') OR (family like 'Вася' AND family like 'Пупкин') OR
        ((name like 'Вася' and family like 'Пупкин') OR (name like 'Пупкин' and family like 'Вася')) 
    
    '''
    def create_filter(words,fields):
        #TODO: нужна оптимизация для исключения повторяющихся условий - сейчас условия повторяются
        filter = None
        if not words or not fields:
            return filter
        
        if len(words) == 0 or len(fields) == 0:
            return filter
        
        if len(words) == 1 and len(fields) == 1:
            filter = Q(**{fields.pop() + '__icontains': words.pop()})
            #filter = '('+fields.pop()+'='+words.pop()+')'
            return filter
        
        if len(words) > 0 and len(fields) == 1:
            field = fields.pop()
            for word in words:
                fltr = Q(**{field + '__icontains': word})
                filter = filter & fltr if filter else fltr
                #fltr = '('+field+'='+word+')'
                #filter = filter+' and '+fltr if filter else fltr
            return filter
        
        for word in words:
            filtr = None
            for field in fields:
                sub_fltr = create_filter(set(words)-set([word]),set(fields)-set([field]))
                if sub_fltr:
                    fltr = (Q(**{field + '__icontains': word}) & sub_fltr)
                    #fltr = '('+field+'='+word+' and '+sub_fltr+')'
                else:
                    fltr = Q(**{field + '__icontains': word})
                    #fltr = '('+field+'='+word+')'
                filtr = (filtr | fltr) if filtr else fltr
                #filtr = '('+filtr+' or '+fltr+')' if filtr else fltr
            filter = (filter | filtr) if filter else filtr
            #filter = '('+filter+' or '+filtr+')' if filter else filtr
        return filter

    if filter_text:
        words = filter_text.strip().split(' ')
        condition = None
        for field_name in fields:
            field_condition = None
            for word in words:
                q = Q(**{field_name + '__icontains': word})
                field_condition = field_condition & q if field_condition else q            
            condition = condition | field_condition if condition else field_condition
        
        # дополнительное условие, если встречаются объединение слов
        cond = create_filter(set(words),set(fields))
        if cond:
            condition = condition | cond if condition else cond
        return condition
    else:
        return None
    