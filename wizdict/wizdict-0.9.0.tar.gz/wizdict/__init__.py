# -*- coding: utf-8 -*-
'''
Created on 8 Jan 2011

@author: G.Bronzini
'''
__VERSION__ = '0.9.0'

class newstring(str):
    def __str__(self):
        return super(newstring, self).__str__()


def group_list(list_of_list, _index):
    """ searches trough a list of lists and returns a dict
        where the keys are the distinct values found in the
        lists at _index position and the values are all the lists
        having the same value for the _index.
        If some of the lists do not have the enough items
        they get grouped in a list with key "_noindex_"

        _index argument may be a callable who will return the
        calculated key when given the current dictionary

        _index argument may also be a list or tuple. groupList will
        create a key with the values for all members of the list
        or tuple (that can also be callables)

        >>> group_list([['a',1], ['b',2],['c',3]], 1)
        {1: [['a', 1]], 2: [['b', 2]], 3: [['c', 3]]}

        >>> group_list([['a',1], ['b',2], ['c',3], ['b',5]]], 0)
        {'a': [['a', 1]], 'c': [['c', 3]], 'b': [['b', 2], ['b', 5]]}

        >>> group_list([['a',1], ['a',2], ['a',3]], 'a')
        {'_noindex_': [['a', 1], ['a', 2], ['a', 3]]}

        >>> group_list([['a',1], ['a',2], ['a',3]], 0)
        {'a': [['a', 1], ['a', 2], ['a', 3]]}
    """

    diz = {}
    errors = []
    for clist in list_of_list:
        if callable(_index):
            ls = diz.setdefault(_index(clist), [])
        elif type(_index) in [list, tuple]:
            newkey = []
            for i in _index:
                if callable(i):
                    res = i(clist)
                else:
                    res = clist[i]
                newkey.append(res)
            ls = diz.setdefault(tuple(newkey), [])
        else:
            if len(clist) < _index:
                ls = errors
            else:
                ls = diz.setdefault(clist[_index], [])
        ls.append(clist)
    if errors:
        diz['_noindex_'] = errors
    return diz


def group_dict(diz_list, _key):
    """ searches trough a list of dict and returns a dict
        where the keys are the distinct values found in the
        dictionaries for the key received as "_key" argument
        and the values are all the dictionaries having the
        same value for the _key.
        If some of the dictionaries do not have the "_key"
        key they get grouped in a list with key "_nokey_"

        _key argument may be a callable who will return the
        calculated key when given the current dictionary

        _key argument may also be a list or tuple. groupDict will
        create a key with the values for all members of the list
        or tuple (that can also be callables)
    """
    diz = {}
    errors = []
    for d in diz_list:
        if callable(_key):
            ls = diz.setdefault(_key(d), [])
        elif type(_key) in [list, tuple]:
            newkey = []
            for l in _key:
                if callable(l):
                    res = l(d)
                else:
                    res = d[l]
                newkey.append(res)
            ls = diz.setdefault(tuple(newkey), [])
        else:
            if not _key in d:
                ls = errors
            else:
                ls = diz.setdefault(d[_key], [])
        ls.append(d)
    if errors:
        diz['_nokey_'] = errors
    return diz


def get_dicts(diz_list, func=None, **kwargs):
    """ searches trough a list of dict and return a list
        of all those dictionaries verifying either of the following
        conditions:
        - func is a boolean returning function to be applied to
          current dictionary to determine if it is to be selected
        - kwarg is a key=value list that has to match key=value
          items of the current dictionary. values of the
          kwargs may be boolean returning callables. kwargs are
          evaluated in AND.
    """
    diz = []
    for d in diz_list:
        if func:
            if func(d):
                diz.append(d)
        else:
            selected = True
            for k, v in kwargs.items():
                if not k in d or d[k] != v:
                    selected = False
                    break
            if selected:
                diz.append(d)
    return diz


def group_stats(d, **kwargs):
    """ Elabora raggruppamenti su liste di dizionari in un dizionario.

    group_stats({ 1: [ {'a': 5, 'b': 2}, {'a': None, 'b': 3, 'c' : 6} ],}, a=lambda x: GroupSum(null_value=7), b=GroupAvg) ==
      { 1: {'a' : 12} , {'b': 2.5} }
    """
    newdict = {}
    for masterkey,dictlist in d.items():
        newdict[masterkey] = {}
        if len(dictlist)>0:
            for key, aggregator_factory in kwargs.items():
                obj = aggregator_factory()
                newdict[masterkey][key] = obj
        for i in dictlist:
            for key in kwargs.keys():
                newdict[masterkey][key].append_value(i[key])
        for key,aggregator in newdict[masterkey].items():
            for fprefix, value in aggregator.get_result_dict().items():
                newdict[masterkey]["%s_%s" % (fprefix, key)]=value
            # newdict[masterkey]["%s%s" % (aggregator.prefix, key)]=aggregator.get_value()
            del newdict[masterkey][key]
    return newdict


def analyze_dict_list(dict_list, attribute_list, grouped=False):
    """ Collect stats from a list of dictionaries on each attribute specfied in an attribute list.
     It will collect min, max, avg, med
     If the attribute name is prefixe with a "-" min and max are swapped

    :param dict_list:
    :param attribute_list:
    :param grouped:
    :return:
    """
    reversed_attrs = filter(lambda x: x.startswith('-'), attribute_list)
    attribute_list = map(lambda x: x[1:] if x.startswith('-') else x, attribute_list)
    reversed_attrs = map(lambda x: x[1:], reversed_attrs)

    grouped_ret, ret = {}, {}
    for attr in attribute_list:
        tmplist = filter(lambda x: x!=None, [x[attr] for x  in dict_list])
        ret["%s_cnt" % attr] = len(tmplist)
        if ret["%s_cnt" % attr]>1:
            ret["%s_sum" % attr] = sum(tmplist)
            ret["%s_min" % attr] = reduce(lambda x,y: x if x<y else y, tmplist)
            ret["%s_max" % attr] = reduce(lambda x,y: x if x>y else y, tmplist)
            ret["%s_avg" % attr] = float(ret["%s_sum" % attr]) / ret["%s_cnt" % attr]
            ret["%s_med" % attr] = reduce(lambda x,y: x if x<y else y, filter(lambda x: x>=ret["%s_avg" % attr], tmplist) )
        elif ret["%s_cnt" % attr]==1:
            ret["%s_sum" % attr], ret["%s_min" % attr], ret["%s_max" % attr], ret["%s_avg" % attr], ret["%s_med" % attr] = tmplist[0], tmplist[0], tmplist[0], tmplist[0], tmplist[0]

        if attr in reversed_attrs:
            ret["%s_min" % attr], ret["%s_max" % attr] = ret["%s_max" % attr], ret["%s_min" % attr]

        if grouped:
            grouped_ret[attr] = ret
            ret ={}

    return grouped_ret if grouped else ret


def batch(iterable, n = 1):
    """ generator splitting an iterable in n elements (defaults=1)
    """
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx+n, l)]