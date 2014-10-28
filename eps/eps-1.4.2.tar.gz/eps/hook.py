
import sys
import inspect
from functools import partial


if hasattr(inspect, 'getfullargspec'):
    getargspec = inspect.getfullargspec
else:
    getargspec = inspect.getargspec


class Looper(object):
    def __init__(self, inst, name):
        self._name_of_method = name
        self.result = None
        self.stop = False
        self.filter = None
        self.eps = inst

    def __call__(self, *argv, **kargs):
        self.line = iter(self.eps._api[self._name_of_method])
        self.argv = argv
        self.kargs = kargs
        self.loop_line()
        return self.result

    def loop_line(self):
        for cfg in self.line:
            if self.stop:
                break
            if cfg['filter']:
                if self.filter:
                    if self.filter not in cfg['filter']:
                        continue
                else:
                    continue
            if cfg['need_self']: r = cfg['method'](self, *self.argv, **self.kargs)
            else: r = cfg['method'](*self.argv, **self.kargs)
            if r is not None: self.result = r

DefaultLooper = Looper


def looper_exec(inst, name, *argv, **kargs):
    return DefaultLooper(inst, name)(*argv, **kargs)


def _apibind(instance, name, method, priority=0, single=False, **kargs):
    """(need_self=False, comment="", filter=None). Bind method to EPS."""
    if name not in instance._api:
        instance._api[name] = line = []
        is_new = True
    else:
        line = instance._api[name]
        is_new = False
        # check for single
        if single:
            raise Exception('Trying to make a single method')
    
    need_self = False
    if method:
        # check for single mode
        for i in line:
            if i['single']:
                raise Exception('Trying to extend a single method')
        # detect self argument
        if 'need_self' in kargs:
            need_self = kargs['need_self']
        elif inspect.isfunction(method):
            margs = getargspec(method).args
            need_self = len(margs) and margs[0] == 'self'
        
        cfg = {}
        cfg['method'] = method
        cfg['priority'] = priority
        cfg['need_self'] = need_self
        cfg['comment'] = kargs.get('comment', None)
        cfg['single'] = single
        # filter
        ff = kargs.get('filter', None)
        if ff:
            cfg['filter'] = ff if isinstance(ff, list) else [ff]
        else:
            cfg['filter'] = None
        
        # detect located
        frame = sys._getframe(1)
        lineno = frame.f_lineno
        filename = inspect.getsourcefile(frame) or inspect.getfile(frame)
        cfg['located'] = filename, lineno

        line.append(cfg)
    
    # looper for need_self
    if need_self or not method:
        is_new = False
    
    # append to EPS
    ns = name.split('.')
    if name not in instance._api_looper:
        p = instance
        for i, k in enumerate(ns):
            if i+1 == len(ns):
                if is_new:
                    t = method
                    if hasattr(p, k):
                        raise Exception('collision - ' + name)
                else:
                    t = partial(looper_exec, instance, name)
                    instance._api_looper.add(name)
            else:
                t = getattr(p, k) if hasattr(p, k) else CNode()
            setattr(p, k, t)
            p = t
    
    # sort queue
    if len(line) > 1:
        instance._api[name] = sorted(line, key=lambda x:x['priority'])


class CNode(object):
    def __getitem__(self, key):
        return getattr(self, key)


class CEPS(CNode):
    def __init__(self):
        self._api = {}
        self._api_looper = set()
        _apibind(self, 'bind', partial(_apibind, self))

    def __getitem__(self, key):
        return getattr(self, key)

