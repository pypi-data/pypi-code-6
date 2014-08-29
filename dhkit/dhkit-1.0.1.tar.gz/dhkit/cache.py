#coding:utf8

"""
Created on 14-5-7

@author: tufei
@description:
         
Copyright (c) 2013 infohold inc. All rights reserved.
"""
import inspect
import cPickle
import string
import functools
import redis


class Cache(object):

    def exists(self, name):
        pass

    def get(self, name):
        pass

    def set(self, name, value, expire_time=None):
        pass

    def delete(self, name):
        pass


class MemCache(Cache):

    __dictionary = dict()

    def exists(self, name):
        return self.__dictionary.has_key(name)

    def get(self, name):
        return self.__dictionary.get(name)

    def set(self, name, value, expire_time=None):
        self.__dictionary[name] = value

    def delete(self, name):
        try:
            self.__dictionary.pop(name)
        except:
            import traceback
            traceback.print_exc()
            pass


class RedisCache(Cache):

    __pool = None

    __conn_args = {
        'host': 'localhost',
        'port': 6379,
        'timeout': 10,
        'max_connections': 50,
    }

    def __init__(self):
        super(RedisCache, self).__init__()
        self.redis_cli = redis.Redis(connection_pool=self.get_pool())

    def exists(self, name):
        return self.redis_cli.exists(name)

    def get(self, name):
        redis_type = self.redis_cli.type(name)
        if redis_type == 'none':
            return None
        elif redis_type == 'hash':
            return self.redis_cli.hgetall(name)
        else:
            return self.redis_cli.get(name)

    def set(self, name, value, expire_time=None):
        pipe = self.redis_cli.pipeline()
        if isinstance(value, dict):
            pipe.hmset(name, value)
        else:
            pipe.set(name, str(value))
        if expire_time is not None:
            pipe.expire(name, expire_time)
        pipe.execute()

    def delete(self, name):
        self.redis_cli.delete(name)

    @classmethod
    def set_conn_config(cls, conn_dict):
        for k in cls.__conn_args:
            if conn_dict.has_key(k):
                cls.__conn_args[k] = conn_dict[k]

    @classmethod
    def get_pool(cls):
        if cls.__pool is None:
            cls.__pool = redis.BlockingConnectionPool(**cls.__conn_args)
        return cls.__pool


VALID_CHARS = set(string.ascii_letters + string.digits + '_.')
DEL_CHARS = ''.join(c for c in map(chr, range(256)) if c not in VALID_CHARS)


class CacheName(object):

    TYPE_CLS_METHOD = 1  # 类方法类型
    TYPE_IST_METHOD = 2  # 实例方法类型
    TYPE_GEN_METHOD = 3  # 普通方法类型

    @classmethod
    def get_func_type(cls, func):
        m_args = inspect.getargspec(func)[0]
        if m_args:
            if m_args[0] == 'cls':
                return cls.TYPE_CLS_METHOD
            if m_args[0] == 'self':
                return cls.TYPE_IST_METHOD
        return cls.TYPE_GEN_METHOD

    @classmethod
    def get_name_prefix(cls, func, *args):
        func_type = cls.get_func_type(func)
        if hasattr(func, '__qualname__'):
            name = func.__qualname__
        else:
            kclass = getattr(func, '__self__', None)
            if kclass and not inspect.isclass(kclass):
                kclass = kclass.__class__
            if not kclass:
                kclass = getattr(func, 'im_class', None)

            if not kclass:
                if func_type == cls.TYPE_IST_METHOD:
                    kclass = args[0].__class__
                elif func_type == cls.TYPE_CLS_METHOD:
                    kclass = args[0]

            # TODO: 目前暂时无法获取静态方法所属类
            if kclass:
                name = "%s.%s" % (kclass.__name__, func.__name__)
            else:
                name = func.__name__
        name_prefix = "cache:%s.%s" % (func.__module__, name.translate(None, DEL_CHARS))
        return name_prefix, func_type

    @classmethod
    def get_func_args_key(cls, func_type, *args, **kwargs):
        arg_values = set()
        n_args = args
        if func_type == cls.TYPE_IST_METHOD or func_type == cls.TYPE_CLS_METHOD:
            n_args = args[1:]
        for arg in n_args:
            arg_values.add(str(arg))
        for kwarg in kwargs:
            arg_values.add(str(kwargs[kwarg]))
        return "_".join(arg_values)

    @classmethod
    def get_by_function(cls, func, *func_args, **func_kwargs):
        """根据func的函数名和参数来生成缓存key名
        :param func: 函数对象
        :param func_args: 函数位置参数
        :param func_kwargs: 函数关键字参数
        :return: string -- 缓存key名
        """
        ns, func_type = cls.get_name_prefix(func, *func_args)
        args_key = cls.get_func_args_key(func_type, *func_args, **func_kwargs)
        if args_key:
            return ns, "%s:%s" % (ns, args_key)
        else:
            return ns, ns

    @classmethod
    def get_by_function_and_ns(cls, ns, func, *func_args, **func_kwargs):
        """根据指定的ns和func的参数来生成缓存key名
        :param ns: 指定的名字空间（前缀）
        :param func: 函数对象
        :param func_args: 函数位置参数
        :param func_kwargs: 函数关键字参数
        :return: string -- 缓存key名
        """
        args_key = cls.get_func_args_key(cls.get_func_type(func), *func_args, **func_kwargs)
        return "%s:%s" % (ns, args_key) if args_key else ns


CACHE_GET = 1
CACHE_DELETE = 2


def cacheable(name=None, expire=300, action=CACHE_GET, cache_cls=RedisCache):
    def _cacheable(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache = cache_cls()

            if action == CACHE_GET:
                ns, cache_key = CacheName.get_by_function(func, *args, **kwargs)
                cache_value = cache.get(cache_key)
                if cache_value is not None:
                    return cPickle.loads(cache_value)
                result = func(*args, **kwargs)
                if result is None:
                    return result
                cache.set(cache_key, cPickle.dumps(result), expire)
                if name is not None:
                    cache.set("cache:alias:%s" % name, ns)  # 存储缓存ns的别名
                return result
            elif action == CACHE_DELETE:
                result = func(*args, **kwargs)
                if name is not None:
                    ns = cache.get("cache:alias:%s" % name)
                    cache_key = CacheName.get_by_function_and_ns(ns, func, *args, **kwargs)
                    cache.delete(cache_key)
                return result
        return wrapper
    return _cacheable
