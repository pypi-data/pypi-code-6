import re


def parse(dict):
    subd = {}
    for key, value in dict.items():
        keys = re.split('(\[|\])', key)
        keys = [x for x in keys if x not in ['[', ']', '']]
        subd = __insert(subd, keys, value)
    return subd


def __insert(dict, keys, value):
    if len(keys) == 1:
        dict[keys[0]] = value
    else:
        if dict.has_key(keys[0]):
            dict[keys[0]] = __insert(dict[keys[0]], keys[1:], value)
        else:
            dict[keys[0]] = __insert({}, keys[1:], value)
    return dict
