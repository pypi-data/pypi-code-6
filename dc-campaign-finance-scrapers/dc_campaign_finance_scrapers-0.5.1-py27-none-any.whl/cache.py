import shelve
import functools
import tempfile
import os
import weakref


PERSISTANT_CACHE = False


def _named_temp_file(name):
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, name)


CACHE_FILE_NAME = _named_temp_file('dc_campaign_finance_scraper')


def use_persistant_cache():
    global PERSISTANT_CACHE
    PERSISTANT_CACHE = True


def clear_persistant_cache():
    with shelve.open(CACHE_FILE_NAME, writeback=True) as cache:
        cache.clear()


def cache():
    if PERSISTANT_CACHE:
        return _persistant_cache(CACHE_FILE_NAME)
    return functools.lru_cache(maxsize=None)


def _check_cache(cache, key, func, args, kwargs):
    return cache.setdefault(key, func(*args, **kwargs))

_handle_dict = weakref.WeakValueDictionary()


def _persistant_cache(filename):
    def decorating_function(user_function):
        def wrapper(*args, **kwds):

            key = str(hash(functools._make_key(args, kwds, typed=False)))

            try:
                print("Using open handle")
                return _check_cache(_handle_dict[filename], key, 
                                    user_function, args, kwds)
            except KeyError:
                print("Opening handle")
                with shelve.open(filename, writeback=True) as cache:
                    _handle_dict[filename] = cache
                    _check_cache(cache, key, user_function, args, kwds)

        return functools.update_wrapper(wrapper, user_function)

    return decorating_function
