#coding:utf-8
'''
Created on 28.10.2010

@author: akvarats
'''

from m3.data.caching import RuntimeCache

class CustomCache0(RuntimeCache):
    pass

class CustomCache1(RuntimeCache):
    '''
    Кеш со встроенным хендлером
    '''
    def handler(self, cache, dimensions):
        return {dimensions: dimensions[0]+1}
    
class CachedDataObject(object):
    def __init__(self, value=None):
        self.value = value

def custom_cache_handler0(cache, dimensions):
    '''
    Сборка данных для кастомного кеша.
    
    Данные для кеша возвращаются из хендлера в виде словаря
    '''
    result = {}
    result[dimensions] = dimensions
    return result
    
    
def custom_cache_handler1(cache, dimensions):
    data = custom_cache_handler0(cache, dimensions)
    for k,v in data.iteritems():
        cache.set(k,v)

CustomCache0().register_handler(custom_cache_handler0)        
RuntimeCache().register_handler(custom_cache_handler1)