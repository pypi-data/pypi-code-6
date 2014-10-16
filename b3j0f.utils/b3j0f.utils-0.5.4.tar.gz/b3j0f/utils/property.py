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

In preserving binding from inheritance and automatical mechanisms which prevent
to set any attribute on any elements.

When you are looking for an element bound property, the result is a dictionary
of the shape {element, {property name, property}}.

.. warning:

    - None methods can not be bound to properties.
    - It is adviced to delete properties from cache after deleting them at
        runtime in order to avoid memory leak.
"""

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

    :return: dictionary of property by name embedded into elt __dict__ or in
        shared __STATIC_ELEMENTS_CACHE__
    :rtype: dict

    .. limitations::
        Do not work on None methods
    """

    result = None

    # in case of dynamic object
    if hasattr(elt, __DICT__) and isinstance(elt.__dict__, dict):
        result = elt.__dict__.setdefault(__B3J0F__PROPERTIES__, {})
    else:
        result = __STATIC_ELEMENTS_CACHE__.setdefault(elt, {})

    return result


def get_properties(elt, *keys):
    """
    Get elt properties.

    :param elt: element form where get properties.
    :param keys: keys of properties to get from elt.

    :return: dict of properties by elt and name.
    :rtype: dict

    .. limitations::
        Do not work on None methods
    """

    result = _get_properties(elt, keys, local=False, forbidden=set())

    return result


def get_property(elt, key, default=None):
    """
    Get one property related to one input key

    :param elt: elt from where get property
    :param str key: property key to get
    :param default: default value to return if key does not exist in elt
        properties
    """

    result = default

    property_elts = get_properties(elt, key)

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


def get_local_properties(elt, *keys):
    """
    Get local elt properties (not defined in elt type or base classes).

    :param elt: element form where get properties.
    :param keys: keys of properties to get from elt.

    :return: dict of properties by name.
    :rtype: dict

    .. limitations::
        Do not work on None methods
    """

    result = _get_properties(elt, keys, local=True, forbidden=set())

    return result


def get_local_property(elt, key, default=None):
    """
    Get one local property related to one input key or default value if key is
        not found

    :param elt: elt from where get property
    :param str key: property key to get
    :param default: default value to return if key does not exist in elt
        properties
    """

    result = default

    local_properties = get_local_properties(elt, key)

    if key in local_properties:
        result = local_properties[key]

    return result


def _get_properties(elt, keys, local, forbidden):
    """
    Get a dictionary of elt properties.

    :param elt: element form where get properties.
    :param keys: keys of properties to get from elt.
    :param bool local: if False, get properties from bases classes and type
        as well.
    :param set forbidden: elts from where not get properties.

    :return: dict of properties:
        - if local: {name, value}
        - if not local: {elt, {name, value}}
    :rtype: dict

    .. limitations::
        Do not work on None methods
    """

    result = OrderedDict()

    # add elt in forbidden in order to avoid to get elt properties twice
    forbidden.add(elt)

    # get property_component_owner such as elt by default
    property_component_owner = elt

    # get bound method properties and put them with instance such as keys
    if ismethod(elt) and elt.__self__ is not None:
        property_component_owner = elt.__self__

    # get property component
    property_component = _get_property_component(property_component_owner)

    # if elt exists in property component
    if elt in property_component:

        properties = property_component[elt]
        if properties:
            result[elt] = OrderedDict()
            for key in keys:
                if key in properties:
                    result[elt][key] = properties[key]
            if not keys:
                result[elt] = properties.copy()

    # if not local, get properties from
    if not local:

        # class
        if hasattr(elt, __CLASS__):
            elt_class = elt.__class__
            if elt_class not in forbidden:
                elt_class_properties = _get_properties(
                    elt_class, keys, local, forbidden
                )
                result.update(elt_class_properties)

        # base method if elt is a method
        if ismethod(elt) and elt.__self__ is not None:
            instance_class = property_component_owner.__class__
            elt_name = elt.__name__
            method = getattr(instance_class, elt_name)
            method_properties = _get_properties(
                method, keys, local, forbidden
            )
            result.update(method_properties)

        # bases classes
        if hasattr(elt, __BASES__):
            for base in elt.__bases__:
                if base not in forbidden:
                    base_result = _get_properties(
                        base, keys, local, forbidden
                    )
                    result.update(base_result)

        # type
        elt_type = type(elt)
        if elt_type is not elt and elt_type not in forbidden:
            elt_type_result = _get_properties(
                elt_type, keys, local, forbidden
            )
            result.update(elt_type_result)

    elif elt in result:  # else, result is result[elt]
        result = result[elt]

    return result


def put_properties(elt, ttl=None, **properties):
    """
    Put properties in elt.

    :param elt: elt on where put property.
    :param float ttl: If not None, property time to leave

    .. limitations::
        Do not work on None methods
    """

    # if there have properties to process
    if properties:

        # define a property component owner
        property_component_owner = elt

        # if elt is an instance method, property component owner is instance
        if ismethod(elt) and elt.__self__ is not None:
            property_component_owner = elt.__self__

        # get property component
        property_component = _get_property_component(property_component_owner)

        # set properties
        elt_properties = property_component.setdefault(elt, {})
        for name in properties:
            value = properties[name]
            elt_properties[name] = value

        if ttl is not None:
            args = [elt]
            args += properties.keys()
            timer = Timer(ttl, del_properties, args=args)
            timer.start()


def del_properties(elt, *keys):
    """
    Delete elt property.

    :param keys: property keys to delete from elt. If empty, delete all
        properties.

    .. limitations::
        Do not work on None methods
    """

    property_component_owner = elt

    # if elt is an instance method, put property only on the instance method
    if ismethod(elt) and elt.__self__ is not None:
        property_component_owner = elt.__self__

    property_component = _get_property_component(property_component_owner)

    # if elt properties exist
    if elt in property_component:
        properties = property_component[elt]
        for key in keys:  # delete specific properties
            if key in properties:
                del properties[key]
        # delete all properties
        if not keys:
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
