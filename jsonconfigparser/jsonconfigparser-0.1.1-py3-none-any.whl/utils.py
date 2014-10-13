import shlex

from functools import partial
from inspect import getfullargspec
from operator import setitem

from jsonpath_rw import parse, Root

# command registry that `command` and `call` use
__registry = {}

# At the time of writing the root of JSONpath is $
# However, this may change in the future
root = str(Root())

def command(f):
    '''Stores a function and the names of its arguments in a registry global.
    The function name has underscores stripped out.

    Returns the function unchanged to the namespace.

    :param f function: The function to be wrapped
    '''

    # this makes for nicer CLI/Interperter command names
    # 'add_field' becomes 'addfield'
    name = f.__name__.replace('_', '')

    info = [f]

    # strip the json argument from commands as call explicitly passes it
    info.extend([a for a in getfullargspec(f).args if a != 'json'])

    __registry[name] = tuple(info)
    return f

def call(fname, json, source):
    '''Looks up a function by its name in the registry global and
    extracts the correct agruments from a source (such as an argparse result)
    and calls the function with the json and other arguments. The result is not
    returned to the caller. call returns True if no exceptions are raised and
    any raised exceptions are propogated to the caller.

        ```
        call('addfield', json, args)
        ```

    :param fname str: The string name of the function to be called.
    :param json: A JSON representation
    :param source obj: An object that contains the arguments needed for
        the function being called.

    :returns True:
    '''

    f, *kwargs = __registry.get(fname)
    kwargs = {n:getattr(source, n) for n in kwargs}
    f(json=json, **kwargs)
    return True


def act_on_path(json, path, action):
    '''Converts a JSONpath to a literal path in the JSON
    and preforms an action on the endpoint.

    :param json JSONConfigParser: The JSON representation to act on.
    :param path str: A string representation of a JSONpath endpoint
    :param action: A callable that accepts the penultimate endpoint and the
        index or key of the endpoint as the first two arguments.
        For additional arguments, tools such as `functools.partial` must
        be used.

    :returns: The value of the action called on the endpoint.
    '''

    if path == root:
        return action(json, path)

    def process(item):
        # JSONpath indicies are denoted by [integer]
        # to be converted to a Python integer the brackets
        # must stripped out
        if '[' in item:
            item = item.replace('[', '').replace(']', '')
            item = int(item)
        return item

    *path, final = [process(item) for item in path.split('.') if item != root]

    json = json.data

    for item in path:
        json = json[item]

    return action(json, final)

def set_on_path(json, path, value):
    '''Sets an item at the end of a JSONpath.

    :param json JSONConfigParser: The JSON representation to act on.
    :param path str: A string representation of a JSONpath endpoint
    :param value: The value to set at the JSONpath endpoint
    :returns None:
    '''
    # setitem y u no kwargs?!
    action = lambda j, f, v: setitem(j, f, v)
    action = partial(action, v=value)
    act_on_path(json, path, action)

def list_(captured=None, secondary=None):
    '''Accepts a space separated string and returns a list of values.
    Optionally accepts a secondary callable to convert the list values.

    :param captured str: A space delimited string of values
    :param secondary callable: If provided, this will transform every value
        in this list.
    :return list:

    '''

    if not captured:
        return partial(list_, secondary=secondary)

    captured = shlex.split(captured)

    if secondary:
        captured = [secondary(v) for v in captured]

    return captured


def dict_(captured=None, secondary=None):
    '''Accepts a space delimited string and breaks them into k=v pairs.

        ```
        dict_("key=value color=purple name=justanr")
         -> dict('key':'value', 'color':'purple', 'name':'justanr')

        ```

    Optionally accepts a secondary callable for converting either
    the key or the value. The callable must accept and return both.
    If the conversion fails, it must raise only AttributeError,
        TypeError or ValueError.

    :param captured str: A space delimited string of key=value pairs.
    :param secondary callable: If provided, this will convert the key value
        pair. It must accept both the key and value as input even if
        it only manipulates one.
    :returns dict:
    '''

    if not captured:
        return partial(dict_, secondary=secondary)


    captured = shlex.split(captured)
    captured = [kv.split('=') for kv in captured]

    # corner case where secondary=dict
    # this probably just pushes the corner case down
    # on more level through :/
    # TODO: Definitive fix if possible
    captured = [(k, '='.join(v)) for k, *v in captured]

    if secondary:
        captured = [secondary(k,v) for k,v in captured]

    return dict(captured)

def bool_(captured):
    '''Simply converts a string to a boolean.

    :param captured str: A string representation of True or False
    :returns boolean:
    '''

    captured = captured.lower()
    if any(f == captured for f in ['false', '0', '0.0']):
        return False
    return True

def build_converter(parts):
    '''Accepts a space delimited string and attempts to build a converter
    out of it.

        ```
        build_converter('int') -> builtins.int
        build_converter('int')('4') -> 4

        build_converter('dict') -> jsonconfigparser.utils.dict_
        build_converter('dict')('key=value') -> {'key':'value'}

        build_converter('dict float') -> functools.partial(
            jsonconfigparser.utils.dict_
            secondary=lambda k,v: (k, builtins.float(v))
            )
        build_converter('dict float')('key=4') -> {'key':4.0}

        build_converter('list int') -> functools.partial(
            jsonconfigparser.utils.list_,
            secondary=builtins.int
            )
        build_converter('list int')('1 2 3') -> [1, 2, 3]

        build_converter('dict int list') -> functools.partial(
            jsonconfigparser.utils.dict_,
            secondary=lambda k,v: (
                int(k),
                jsonconfigparser.utils.list_(v)
                )
            )
        build_converter('dict int list')('0="a b c") ->
            {0:['a', 'b', c']

        # the killing joke
        build_converter('dict int dict int list') -> functools.partial(
            jsonconfigparser.utils.dict_,
            secondardy=lambda k,v: (
                int(k),
                jsonconfigparser.utils.dict_(
                    secondary=lambda k,v: (
                        int(k),
                        jsonconfigparser.utils.list_
                        )
                    )
                )
            )
        build_converter('dict int dict int list')('4="4=\'a b c\'"') ->
            {4: {4: ['a', 'b', 'c']}}
        ```

    There are certain basic rules in place:
        * If a blank string or list is passed in, the string type is returned
        * If even one of the values passed in isn't in the mapping,
            the string type is returned
        * If a list is the first value, it's secondary converter is built
            from the remainder of the parts
        * If a dict is the first value, it's secondary converter is built by:
            1 If there is only one following part or the next part is either
                a list or a dictionary, only the values are converted and the
                converter is built from the remainder of the parts
            2 If there are multiple parts remaining and the next part is not
                either a list or a dict, then both the keys and the values are
                manipulated. The key converter is the next part in the list and
                the value converter is built from the remainder of the parts
        * If more than one value is passed in and the head is not a list or
            a dict, then the string type is returned.

    :param parts: Either a string delimited by space or a list of strings.
    :returns callable:
    '''

    nonscalar = ['list', 'dict']

    if not isinstance(parts, list):
        # likely the first time through
        # so parts needs to be transformed
        # into a list
        parts = shlex.split(parts)

    if not parts:
        # we recieved a Falsey value
        # instead of blowing up
        # return the string type
        return fieldtypes['str']

    if not all(p in fieldtypes for p in parts):
        # Something in the parts list isn't a valid
        # fieldstype key, so we'll simply return
        # the string type and call it a day
        #
        # TODO: Does raising an error make more sense?
        return fieldtypes['str']

    if len(parts) == 1:
        # The easiest actual case to handle
        # Just return the matching converter
        #
        # ex: build_converter('int')
        return fieldtypes[parts[0]]

    else:
        if parts[0] == 'list':
            # builds a list converter and the secondary
            # converter is constructed from the remainder
            # of the parts
            #
            # ex: build_converter('list int')
            return fieldtypes['list'](secondary=build_converter(parts[1:]))

        elif parts[0] == 'dict':

            if len(parts[1:]) == 1 or any(ns == parts[1] for ns in nonscalar):
                # If there is only one more part -OR- the next part is
                # a list or dictionary, we'll only build a converter
                # for the values of this dictionary
                #
                # ex: build_converter('dict list int')
                # ex: build_converter('dict dict')
                return fieldtypes['dict'](
                    secondary=lambda k,v: (
                        k,
                        build_converter(parts[1:])(v)
                        )
                    )
            else:
                # More than one converter remaining -AND- the next converter
                # is not a list or dict, then build a secondary converter that
                # manipulates both the key and the value. The key is converted
                # by the next converter and the value converter is built from
                # the rest of the parts
                #
                # ex: build_converter('dict int list')
                return fieldtypes['dict'](
                    secondary=lambda k,v: (
                        build_converter(parts[1])(k),
                        build_converter(parts[2:])(v)
                        )
                    )
        else:
            # We were passed something that doesn't make
            # sense, for now just return the string converter
            #
            # ex: build_converter('int float')
            return fieldtypes['str']

# dictionary of callables that return JSON compliant types
fieldtypes = {
    'bool'  : bool_,
    'str'   : str,
    'int'   : int,
    'list'  : list_,
    'dict'  : dict_,
    'float' : float,
    }
