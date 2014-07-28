import os

def here(*segments):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *segments)

def slugify(s, separator='_'):
    return s.lower().replace(' ', separator)

def first(l):
    return l[0]

def deflate(obj, skip=[], connector='_', parent_key=''):
    items = []

    for sub_key, v in obj.items():
        if parent_key:
            key = parent_key + connector + sub_key
        else:
            key = sub_key

        if isinstance(v, dict) and not (key in skip):
            items.extend(deflate(v, skip, connector, key).items())
        elif isinstance(v, list):
            items.append((key, v))
        else:
            items.append((key, v))

    return dict(items)
