#coding:utf-8
'''
Created on 19.02.2011

@author: akvarats
'''

#===============================================================================
# Общие функции получения объектов из базы данных
#===============================================================================
def get_object_by_id(model, object_id):
    '''
    Возвращает объект из базы данных указанного типа и 
    указанным идентификатором. В случае, если в object_id
    оказался объект типа model, то он и возвращается.
    '''
    result = None
    
    if isinstance(object_id, (int, str, unicode)):
        try:
            result = model.objects.get(pk=object_id)
        except model.DoesNotExist:
            result = None
    elif isinstance(object_id, model):
        result = object_id
        
    return result