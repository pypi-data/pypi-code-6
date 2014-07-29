__options = {
    'p': '\033[95m',
    'c': '\033[94m',
    'y': '\033[93m',
    'g': '\033[92m',
    'r': '\033[91m',
    'b': '\033[1m',
    'x': '\033[0m'
}


def prettify(thing, depth=4):
    if type(thing) is dict:
        formatted = '{'
        for key in thing:
            formatted += '\n' + (' ' * depth) 
            formatted += key + ': ' + prettify(thing[key], depth + 4) + ','
        formatted = formatted[:-1]
        formatted += '\n' + (' ' * (depth - 4)) + '}'
        return formatted
    elif type(thing) is tuple:
        formatted = '('
        for element in thing:
            formatted += '\n' + (' ' * depth)
            formatted += prettify(element, depth + 4) + ','
        formatted += '\n' + (' ' * (depth - 4)) + ')'
        return formatted
    elif type(thing) is list:
        formatted = '['
        for element in thing:
            formatted += '\n' + (' ' * depth)
            formatted += prettify(element, depth + 4) + ','
        formatted = formatted[:-1]
        formatted += '\n' + (' ' * (depth - 4)) + ']'
        return formatted
    return str(thing)


def log(thing, options=''):
    options = [__options[option] for option in options if option in __options]
    prefix = ''.join(options)
    print prefix + prettify(thing) + __options['x']