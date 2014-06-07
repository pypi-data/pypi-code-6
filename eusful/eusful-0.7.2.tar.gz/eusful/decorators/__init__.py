def cache_result(func, *args, **kwargs):
  """
  This code considers any iterable type (e.g. tuple, list) whose constituent elements are identical as identical.
  In theory this could cause a function decorated with cache_result to incorrectly return the result of a call with
  other parameters, but in practice you would need to write a function that deliberately behaves differently depending
  on the particular type of iterable, and then deliberately decorate it with cache_result, and then deliberately call it
  with params that would exploit this hole.
  There is also unbounded growth with this code.  We could use a version specifically for instance methods where the cache
  will be stored on self, and the key would include the method name; those caches would go away as the objects go away.
  That approach, however, does not work with freestanding functions.
  """
  def make_key_from_obj(obj):
    try:
      hash(obj)
      key = (obj,)
      return key
    except TypeError:
      pass
    if isinstance(obj, dict):
      key = tuple()
      for k, v in obj.items():
        key += (k,) + make_key_from_obj(v)
      return key
    try:
      key = tuple()
      for subobj in iter(obj):
        key += make_key_from_obj(subobj)
      return key
    except:
      raise TypeError('Not hashable, not iterable, not a dict')

  def make_key_from_args(*args, **kwargs):
    return make_key_from_obj(args) + make_key_from_obj(kwargs)

  def get_cached_result(f, *args, **kwargs):
    key = make_key_from_args(*args, **kwargs)
    if not hasattr(f, '_cached_results'):
      f._cached_results = {}
    if not f._cached_results.has_key(key):
      f._cached_results[key] = f(*args, **kwargs)
    return f._cached_results[key]

  def proxy(*args, **kwargs):
    return get_cached_result(func, *args, **kwargs)

  return proxy
