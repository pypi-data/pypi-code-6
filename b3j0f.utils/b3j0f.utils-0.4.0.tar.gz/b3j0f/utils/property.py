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
"""

from inspect import ismethod


__B3J0F__PROPERTIES__ = '__b3j0f_props'  #: __dict__ properties key

__DICT__ = '__dict__'  #: __dict__ elt attribute name
__SELF__ = '__self__'  #: __self__ class instance attribute name
__BASES__ = '__bases__'  # __bases__ class attribute name

__STATIC__DICTS__ = {}  #: dictionary of properties for static objects


def _get_property_component(elt):
    """
    Get property component which could embed properties

    :return: dictionary of property by name embedded into elt __dict__ or in
        shared __STATIC__DICTS__
    :rtype: dict

    .. limitations::
        Do not work on None methods
    """

    result = None

    # in case of dynamic object
    if hasattr(elt, __DICT__) and isinstance(elt.__dict__, dict):
        result = elt.__dict__.setdefault(__B3J0F__PROPERTIES__, {})
    else:
        result = __STATIC__DICTS__.setdefault(elt, {})

    return result


def get_properties(elt, *keys):
    """
    Get elt properties related to input keys where keys are property elts and
        values are property values if keys is None, or dict of property
        name, value if keys is None.

    :param elt: element form where get properties.
    :param keys: keys of properties to get from elt.

    :return: dict of properties.
    :rtype: dict

    .. limitations::
        Do not work on None methods
    """

    result = _get_properties(elt, keys, None)

    return result


def _get_properties(elt, keys, _visited_elts):

    result = {}

    # save visited elts in order to not call this twice on the same elt
    if _visited_elts is None:
        _visited_elts = set()

    _visited_elts.add(elt)

    # get bound method properties and put them with instance such as keys
    if ismethod(elt) and hasattr(elt, __SELF__):
        instance = elt.__self__
        if instance is not None:  # do not manage None methods
            # get instance property component
            property_component = _get_property_component(instance)
            if elt in property_component:
                # instance properties are at instance property component elt
                instance_properties = property_component[elt]
                if instance not in result:
                    result[elt] = {}
                for key in keys:  # get properties from keys
                    result[elt][key] = instance_properties[key]
                else:  # get all properties whatever names
                    if not keys:
                        result[elt] = instance_properties.copy()

            # set elt to class method
            elt_name = elt.__name__
            instance_class = type(instance)
            elt = getattr(instance_class, elt_name)

    # get elt properties
    property_component = _get_property_component(elt)

    # parse properties
    for owner in property_component.keys():
        # delete all inherited properties
        if owner != elt:
            del property_component[owner]
        else:
            # fill result with properties
            owner_properties = property_component[owner]
            if owner not in result:
                result[owner] = {}
            for key in keys:  # get properties from keys
                result[owner][key] = owner_properties[key]
            else:  # get all properties whatever names
                if not keys:
                    result[owner] = owner_properties.copy()

    # get properties of bases classes
    if hasattr(elt, __BASES__):
        for base in elt.__bases__:
            if base not in _visited_elts:
                base_result = _get_properties(base, keys, _visited_elts)
                result.update(base_result)

    # get type properties
    elt_type = type(elt)
    if elt_type is not elt and elt_type not in _visited_elts:
        elt_type_result = _get_properties(elt_type, keys, _visited_elts)
        result.update(elt_type_result)

    return result


def put_properties(elt, **properties):
    """
    Put properties in elt.

    :param elt: elt on where put property.

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
        else:  # delete all properties
            if not keys:
                del property_component[elt]
