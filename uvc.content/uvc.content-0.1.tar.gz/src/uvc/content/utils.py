# -*- coding: utf-8 -*-

from .directives import schema, Fields


def bootstrap_component(component, *ifaces, **values):
    if values and ifaces:
        ifields = Fields(*ifaces)
        for key, value in values.items():
            ifield = ifields.get(key)
            if ifield is None:
                continue
            field = ifield.bind(component)
            field.validate(value)
            field.set(component, value)


def schematic_bootstrap(component, **values):
    ifaces = schema.bind(default=None).get(component)
    if ifaces is not None:
        bootstrap_component(component, *ifaces, **values)
