# -*- coding: utf-8 -*-

"""
Library which aims to bind named properties on any element at runtime.

This module can bind a named property on:

    - not modifiable elements such as builtin or class with __slots__
    - functions
    - modules
    - classes
    - namespaces (class without base class)
    - methods
    - instance methods (except for None methods)
    - instance objects (object(), 1, None, etc).

And can not bind on None methods and unhashable types such as dict or list.

In preserving binding from inheritance and automatical mechanisms which prevent
to set any attribute on any elements.

When you are looking for an element bound property, the result is a dictionary
of the shape {element, {property name, property}}.

.. warning:

    - It is adviced to delete properties from cache after deleting them at
        runtime in order to avoid memory leak.
"""

__all__ = [
    'get_properties', 'get_property', 'get_first_property',
    'get_local_property', 'get_local_properties',
    'put_properties', 'del_properties',
    'unify', 'setdefault', 'free_cache'
]

from b3j0f.utils.version import PY26

if PY26:  # import OrderedDict for python2.6 form ordereddict
    from ordereddict import OrderedDict
else:  # in other cases, import OrderedDict from collections
    from collections import OrderedDict

from inspect import ismethod

try:
    from threading import Timer
except ImportError:
    from dummy_threading import Timer

__B3J0F__PROPERTIES__ = '__b3j0f_props'  #: __dict__ properties key

__DICT__ = '__dict__'  #: __dict__ elt attribute name
__CLASS__ = '__class__'  #: __class__ elt attribute name
__SELF__ = '__self__'  #: __self__ class instance attribute name
__BASES__ = '__bases__'  # __bases__ class attribute name

__STATIC_ELEMENTS_CACHE__ = {}  #: dictionary of properties for static objects


def _find_ctx(ctx, elt):
    """
    Get the right ctx related to ctx and elt.

    In order to keep safe memory as much as possible, it is important to find
    the right context element. For example, instead of putting properties on
    a function at the level of an instance, it is important to save such
    property on the instance because the function.__dict__ is shared with
    instance class function, and so, if the instance is deleted from memory,
    the property is still present in the class memory. And so on, it is
    impossible to identify the right context in such case if all properties
    are saved with the same key in the same function which is the function.
    """

    result = ctx  # by default, result is ctx

    if ctx is None:  # if ctx is None, result is elt
        result = elt

    # if elt is ctx and elt is a method, it is possible to find the best ctx
    if elt is result and ismethod(elt):
        # get instance and class of the elt
        instance = elt.__self__
        # if instance is not None, the right context is the instance
        if instance is not None:
            result = instance

    return result


def free_cache(*elts):
    """
    Free properties bound to input cached elts. If empty, free the whole cache.
    """

    global __STATIC_ELEMENTS_CACHE__

    for elt in elts:
        if elt in __STATIC_ELEMENTS_CACHE__:
            del __STATIC_ELEMENTS_CACHE__[elt]

    if not elts:
        __STATIC_ELEMENTS_CACHE__ = {}


def _get_property_component(elt):
    """
    Get property component which could embed properties

    :param elt: property component elt. Not None methods or unhashable types.
    :param ctx: elt ctx from where get properties. Equals elt if None. It
        allows to get function properties related to a class or instance if
        related function is defined in base class.

    :return: dictionary of property by name embedded into elt __dict__ or in
        shared __STATIC_ELEMENTS_CACHE__
    :rtype: dict
    :raises: TypeError if elt is not managed
    """

    result = None

    # in case of dynamic object
    if hasattr(elt, __DICT__) and isinstance(elt.__dict__, dict):
        result = elt.__dict__.setdefault(__B3J0F__PROPERTIES__, {})
    else:
        try:
            result = __STATIC_ELEMENTS_CACHE__.setdefault(elt, {})
        except TypeError:
            # in case of not hashable object
            raise TypeError('elt {0} must be hashable.'.format(elt))
        result = __STATIC_ELEMENTS_CACHE__.setdefault(elt, {})

    return result


def get_properties(elt, keys=(), ctx=None):
    """
    Get elt properties.

    :param elt: properties elt. Not None methods or unhashable types.
    :param keys: keys of properties to get from elt.
    :param ctx: elt ctx from where get properties. Equals elt if None. It
        allows to get function properties related to a class or instance if
        related function is defined in base class.

    :return: dict of properties by elt and name.
    :rtype: dict
    :raises: TypeError if elt is not managed
    """

    result = _get_properties(
        elt, keys=keys, local=False, exclude=set(), ctx=ctx)

    return result


def get_property(elt, key, ctx=None):
    """
    Get properties related to one input key.

    :param elt: property elt. Not None methods or unhashable types.
    :param str key: property key to get.
    :param ctx: elt ctx from where get properties. Equals elt if None. It
        allows to get function properties related to a class or instance if
        related function is defined in base class.
    :raises: TypeError if elt is not managed.
    """

    result = {}

    property_elts = get_properties(elt, keys=(key,), ctx=ctx)

    # parse elements in property elements
    for property_elt in property_elts:
        # get element properties
        elt_properties = property_elts[property_elt]
        # if key in element properties
        if key in elt_properties:
            # set result
            result[property_elt] = elt_properties[key]

    return result


def get_first_property(elt, key, default=None, ctx=None):
    """
    Get first property related to one input key

    :param elt: first property elt. Not None methods or unhashable types.
    :param str key: property key to get.
    :param default: default value to return if key does not exist in elt.
        properties
    :param ctx: elt ctx from where get properties. Equals elt if None. It
        allows to get function properties related to a class or instance if
        related function is defined in base class.

    :raises: TypeError if elt is not managed.
    """

    result = default

    property_elts = get_properties(elt, keys=(key,), ctx=ctx)

    # parse elements in property elements
    for property_elt in property_elts:
        # get element properties
        elt_properties = property_elts[property_elt]
        # if key in element properties
        if key in elt_properties:
            # set result
            result = elt_properties[key]
            # and break the loop
            break

    return result


def get_local_properties(elt, keys=(), ctx=None):
    """
    Get local elt properties (not defined in elt type or base classes).

    :param elt: local properties elt. Not None methods or unhashable types.
    :param keys: keys of properties to get from elt.
    :param ctx: elt ctx from where get properties. Equals elt if None. It
        allows to get function properties related to a class or instance if
        related function is defined in base class.

    :return: dict of properties by name.
    :rtype: dict
    :raises: TypeError if elt is not managed.
    """

    result = _get_properties(
        elt, keys=keys, local=True, exclude=set(), ctx=ctx)

    return result


def get_local_property(elt, key, default=None, ctx=None):
    """
    Get one local property related to one input key or default value if key is
        not found.

    :param elt: local property elt. Not None methods or unhashable types.
    :param str key: property key to get.
    :param default: default value to return if key does not exist in elt
        properties.
    :param ctx: elt ctx from where get properties. Equals elt if None. It
        allows to get function properties related to a class or instance if
        related function is defined in base class.
     :raises: TypeError if elt is not managed.
    """

    result = default

    local_properties = get_local_properties(elt=elt, keys=(key,), ctx=ctx)

    if key in local_properties:
        result = local_properties[key]

    return result


def _get_properties(elt, keys, local, exclude, ctx=None):
    """
    Get a dictionary of elt properties.

    Such dictionary is filled related to the elt properties, and from all base
        elts properties if not local.

    :param elt: properties elt. Not None methods or unhashable types.
    :param ctx: elt ctx from where get properties. Equals elt if None. It
        allows to get function properties related to a class or instance if
        related function is defined in base class.
    :param keys: keys of properties to get from elt.
    :param bool local: if False, get properties from bases classes and type
        as well.
    :param set exclude: elts from where not get properties.

    :return: dict of properties:
        - if local: {name, value}.
        - if not local: {elt, {name, value}}.
    :rtype: dict

    :raises: TypeError if elt is not managed.
    """

    result = OrderedDict()

    # get the best context
    ctx = _find_ctx(ctx=ctx, elt=elt)

    # get ctx property component
    property_component = _get_property_component(ctx)

    # if elt exists in property component
    if elt in property_component:
        # get properties
        properties = property_component[elt]
        # if properties exist
        if properties:
            # try to add all property values in result[elt]
            result[elt] = {}
            for key in keys:
                if key in properties:
                    result[elt][key] = properties[key]
            # add all properties if keys is not specified
            if not keys:
                result[elt] = properties.copy()
            # delete result[elt] if empty
            if not result[elt]:
                del result[elt]

    # if not local, get properties from
    if not local:

        # add elt in exclude in order to avoid to get elt properties twice
        exclude.add(elt)

        # and search among bases ctx elements
        if ctx is not elt:
            # go to base elts
            try:
                elt_name = elt.__name__
            except AttributeError:
                pass
            else:
                # if elt is a sub attr of ctx
                if hasattr(ctx, elt_name) and getattr(ctx, elt_name) == elt:
                    if hasattr(ctx, __BASES__):
                        ctx_bases = ctx.__bases__
                    elif hasattr(ctx, __CLASS__):
                        ctx_bases = (ctx.__class__,)
                    else:
                        ctx_bases = ()
                    for base_ctx in ctx_bases:
                        if hasattr(base_ctx, elt_name):
                            base_elt = getattr(base_ctx, elt_name)
                            if hasattr(base_elt, __DICT__):
                                if base_elt.__dict__ is elt.__dict__:
                                    base_properties = _get_properties(
                                        elt=base_elt,
                                        keys=keys,
                                        local=local,
                                        exclude=exclude,
                                        ctx=base_ctx
                                    )
                                    result.update(base_properties)

        else:
            # bases classes
            if hasattr(elt, __BASES__):
                for base in elt.__bases__:
                    if base not in exclude:
                        base_result = _get_properties(
                            elt=base,
                            keys=keys,
                            local=local,
                            exclude=exclude,
                            ctx=base
                        )
                        result.update(base_result)

            # search among type definition

            # class
            if hasattr(elt, __CLASS__):
                elt_class = elt.__class__
                if elt_class not in exclude:
                    elt_class_properties = _get_properties(
                        elt=elt_class,
                        keys=keys,
                        local=local,
                        exclude=exclude,
                        ctx=elt_class
                    )
                    result.update(elt_class_properties)

            # type
            elt_type = type(elt)
            if elt_type is not elt and elt_type not in exclude:
                elt_type_properties = _get_properties(
                    elt=elt_type,
                    keys=keys,
                    local=local,
                    exclude=exclude,
                    ctx=elt_type
                )
                result.update(elt_type_properties)

    elif elt in result:  # else, result is result[elt]
        result = result[elt]

    else:  # if no local property exist, return an empty dict
        result = {}

    return result


def put_property(elt, key, value, ttl=None, ctx=None):

    return put_properties(elt=elt, properties={key: value}, ttl=ttl, ctx=ctx)


def put_properties(elt, properties, ttl=None, ctx=None):
    """
    Put properties in elt.

    :param elt: properties elt to put. Not None methods or unhashable types.
    :param number ttl: If not None, property time to leave.
    :param ctx: elt ctx from where put properties. Equals elt if None. It
        allows to get function properties related to a class or instance if
        related function is defined in base class.
    :param dict properties: properties to put in elt. elt and ttl are exclude.

    :return: Timer if ttl is not None.
    :rtype: Timer

    :raises: TypeError if elt is not managed.
    """

    result = None

    if properties:

        # get the best context
        ctx = _find_ctx(ctx=ctx, elt=elt)

        # get property component
        property_component = _get_property_component(ctx)

        # set properties
        elt_properties = property_component.setdefault(elt, {})
        elt_properties.update(properties)

        if ttl is not None:
            kwargs = {
                'elt': elt,
                'ctx': ctx,
                'keys': tuple(properties.keys())
            }
            result = Timer(ttl, del_properties, kwargs=kwargs)
            result.start()

    return result


def del_properties(elt, keys=(), ctx=None):
    """
    Delete elt property.

    :param elt: properties elt to del. Not None methods or not hashable types.
    :param keys: property keys to delete from elt. If empty, delete all
        properties.

    :raises: TypeError if elt is not managed.
    """

    # get the best context
    ctx = _find_ctx(ctx=ctx, elt=elt)

    property_component = _get_property_component(ctx)

    # if elt properties exist
    if elt in property_component:
        properties = property_component[elt]
        for key in keys:  # delete specific properties
            if key in properties:
                del properties[key]
        # delete all properties if not keys or not properties for memory leak
        if not (keys and properties):
            del property_component[elt]


def unify(properties):
    """
    Transform a dictionary of {elts, {name, value}} (resulting from
        get_properties) to a dictionary of {name, value} where names are first
        encountered in input properties.

    :param OrderedDict properties: properties to unify.
    :return: dictionary of parameter values by names.
    :rtype: dict
    """

    result = {}

    # parse elts
    for elt in properties:
        # get elt properties
        elt_properties = properties[elt]
        # iterate on elt property names
        for name in elt_properties:
            # add property in result only if not already present in result
            if name not in result:
                value = elt_properties[name]
                result[name] = value

    return result


def setdefault(elt, key, default, ctx=None):
    """
    Get a local property and create default value if local property does not
        exist.

    :param elt: local proprety elt to get/create. Not None methods or not \
hashable types.
    :param str key: proprety name.
    :param default: property value to set if key no in local properties.

    :raises: TypeError if elt is not managed.
    """

    # get the best context
    ctx = _find_ctx(ctx=ctx, elt=elt)

    property_component = _get_property_component(ctx)

    elt_properties = property_component.setdefault(elt, {})

    if key not in elt_properties:

        elt_properties[key] = default

    result = elt_properties[key]

    return result
