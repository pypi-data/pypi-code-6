import doctest
from pprint import pprint

def unnest(dct):
    """
    >>> pprint(unnest({'a': 0, 'b': [{'b1': 2, 'b2': 2},]}))
    ({'a': 0, 'b_id': 1}, {'b': [{'b1': 2, 'b2': 2, 'b_id': 1}]})
    """
    for (k, v) in dct.items():
        if isinstance(v, list):
            lst = dct.pop(k)
            for itm in lst:
                id_fields = [key for in itm.keys() if key.lower().endswith('id')]
                id_fields = sorted(id_fields, key=len)
                if not hasattr(itm, 
                
        if
    return (dct, {})
    
if __name__ == '__main__':
    doctest.testmod()
    