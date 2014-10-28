# -*- coding: utf-8 -*-
from __future__ import print_function, division
import importlib
import random
import collections


# printing vectors

spac = '   '
down = '│  '
tndw = '├──'
turn = '└──'

def explorer_ascii(cfg):
    s = _explorers(cfg)
    return ''.join(s)

def _explorers(cfg, prefix=''):
    name = cfg.classname.rsplit('.', 1)[1]
    if name == 'MetaExplorer':
        return _meta_explorer(cfg, prefix=prefix)
    else:
        return _other_explorer(cfg, prefix=prefix)
        return ['{}{}\n'.format(prefix, name)]

def _other_explorer(cfg, prefix=''):
    s = ['{}{}\n'.format(prefix, cfg.classname.rsplit('.', 1)[1])]
    for key, value in cfg._items():
        if key != 'classname':
            s.append('{}    {}: {}\n'.format(prefix, key, value))
    return s

def _meta_explorer(cfg, prefix=''):
    # s = ['{}Mix2\n'.format(prefix)]
    s = ['MetaExplorer\n']
    i = 0
    while 'ex_{}'.format(i) in cfg:
        if 'ex_{}'.format(i+1) in cfg:
            s.append('{}├── {}\n'.format(prefix, _timeline(cfg, i)))
            s.extend(_explorers(cfg['ex_{}'.format(i)], prefix=prefix+'│   '))
            s.append(prefix+'│\n')
        else:
            s.append('{}└── {}\n'.format(prefix, _timeline(cfg, i)))
            s.extend(_explorers(cfg['ex_{}'.format(i)], prefix=prefix+'    '))
        i += 1
    return s

def _timeline(cfg, i):
    s = []
    for era, weights in zip(cfg.eras, cfg.weights):
        s.append('{:3d}% [->{}]'.format(int(100*weights[i]/sum(weights)), 'end' if era is None else era))
    return '[{}]'.format(', '.join(s))

def _load_class(classname):
    """Load a class from a string"""
    module_name, class_name = classname.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


# signals & vectors

def to_vector(signal, channels=None):
    """Convert a signal to a vector"""
    if channels is None:
        # we need consistent ordering
        assert isinstance(signal, collections.OrderedDict)
        return tuple(signal.values())
    else:
        return tuple(signal[c.name] for c in channels)

def to_signal(vector, channels):
    """Convert a vector to a signal"""
    assert len(vector) == len(channels)
    return {c_i.name: v_i for c_i, v_i in zip(channels, vector)}

def random_signal(channels, bounds=None):
    if bounds is None:
        return {c.name: c.fixed if c.fixed is not None else random.uniform(*c.bounds)
                for c in channels}
    else:
        return {c.name: c.fixed if c.fixed is not None else random.uniform(*b)
                for c, b in zip(channels, bounds)}

def avg_signal(channels, bounds=None):
    if bounds is None:
        return {c.name: c.fixed if c.fixed is not None else 0.5*(c.bounds[0]+c.bounds[1])
                for c in channels}
    else:
        return {c.name: c.fixed if c.fixed is not None else 0.5*(b[0]+b[1])
                for c, b in zip(channels, bounds)}

def signal_inbound(signal, channels):
    return all(c.bounds[0] <= signal[c.name] <= c.bounds[1] for c in channels)

def belongs(p, bounds):
    if p is None or bounds is None:
        return False
    assert len(p) == len(bounds)
    return all(b_i[0] <= p_i <= b_i[1] for p_i, b_i in zip(p, bounds))

def print_msignal(m_signal):
    s = ', '.join("'{}': {:+5.2f}".format(key, m_signal[key]) for key in sorted(m_signal.keys()))
    return '{' + '{}'.format(s) + '}'


# probabilities

def roulette_wheel(proba):
    assert len(proba) >= 1
    """Given a vector p, return index i with probability p_i/sum(p).
    Elements of p are positive numbers.
    @param proba    list of positive numbers
    """
    sum_proba = sum(proba)
    dice = random.uniform(0., sum_proba)
    if sum_proba == 0.0:
        return random.randint(0, len(proba)-1)
    s, i = proba[0], 0
    while (i < len(proba)-1 and dice >= s):
        i += 1
        assert proba[i] >= 0, "all elements are not positive {}".format(proba)
        s += proba[i]
    return i


# vectors

def vec_norm(a, b):
    return math.sqrt(sum((a_i-b_i)**2 for a_i, b_i in zip(a, b)))

def vec_norm_sq(a, b):
    return sum((a_i-b_i)**2 for a_i, b_i in zip(a, b))

def sgn_norm(a, b, channels):
    return math.sqrt(sum((a[c]-b[c])**2 for c in channels))

def sgn_norm_sq(a, b, channels):
    return sum((a[c]-b[c])**2 for c in channels)

