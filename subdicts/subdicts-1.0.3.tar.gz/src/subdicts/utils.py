import re


def parse(dictionary):
    subd = {}
    for key, value in dictionary.items():
        keys = re.split('(\[|\])', key)
        keys = [x for x in keys if x not in ['[', ']', '']]
        subd = __insert(subd, keys, value)
    return subd


def __insert(dictionary, keys, value):
    if len(keys) == 1:
        dictionary[keys[0]] = value
    else:
        if keys[0] in dictionary:
            dictionary[keys[0]] = __insert(dictionary[keys[0]], keys[1:], value)
        else:
            dictionary[keys[0]] = __insert({}, keys[1:], value)
    return dictionary
