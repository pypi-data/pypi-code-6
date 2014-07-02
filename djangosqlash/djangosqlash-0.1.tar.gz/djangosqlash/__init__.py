# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from collections import namedtuple


p = Pair = namedtuple("Pair", "left, right")


class S(object):
    atom = "atom"
    array = "array"
    object = "object"


def model_of(ob):
    from django.db.models.base import ModelBase
    if isinstance(ob, ModelBase):
        return ob
    else:
        return ob.__class__


class Control(object):
    def __init__(self):
        self.fieldmap = {}  # class -> fields

    def get_fieldmap_from_model(self, model):
        try:
            return self.fieldmap[model]
        except KeyError:
            fieldmap = self.fieldmap[model] = {f.name: f for f in model._meta.local_fields}
            for f in model._meta.local_many_to_many:
                fieldmap[f.name] = f
            return fieldmap

    def get_property_from_object(self, ob, k):
        fieldmap = self.get_fieldmap_from_model(model_of(ob))
        try:
            return fieldmap[k]
        except KeyError:
            from django.db.models import IntegerField  # xxx
            fieldmap[k] = IntegerField
            return IntegerField

    def get_type_from_property(self, prop):
        if isinstance(prop, type):
            return prop
        else:
            return prop.__class__

    def get_shape_from_object(self, ob, k):
        if k.endswith("_set"):
            return S.array
        else:
            fieldmap = self.get_fieldmap_from_model(model_of(ob))
            from django.db.models import ManyToManyField
            if isinstance(fieldmap[k], ManyToManyField):
                return S.array
            else:
                return S.object


class Abbreviation(object):
    def __init__(self, control):
        self.control = control

    def __call__(self, ob, name):
        from django.db.models import ForeignKey
        if name == "*":
            for f in ob._meta.local_fields:
                if not isinstance(f, ForeignKey):
                    yield f.name
        else:
            yield name
Empty = ()


class SerializerFactory(object):
    def __init__(self, convertions=None, control=Control(), factory=dict):
        self.convertions = convertions or {}
        self.control = control
        self.factory = factory

    def __call__(self, renaming_options=None, abbreviation=Abbreviation):
        return Serializer(
            self.convertions,
            self.control,
            self.factory,
            renaming_options=renaming_options or {},
            abbreviation=abbreviation(self.control)
        )


class Serializer(object):
    def __init__(self, convertions, control, factory, renaming_options, abbreviation):
        self.convertions = convertions
        self.control = control
        self.factory = factory

        self.abbreviation = abbreviation
        self.renaming_options = renaming_options

    def serialize(self, ob, q_collection, renaming_options=None):
        renaming_options = renaming_options or {}
        r = self.factory()
        for q in q_collection:
            for q in self.abbreviation(ob, q):
                self.build(r, *self.parse(ob, q))
        return r

    def parse(self, ob, q):
        if isinstance(q, Pair):
            k = q.left
            prop = self.control.get_property_from_object(ob, k)
            shape = self.control.get_shape_from_object(ob, k)
            if shape == S.array:
                sub_r = [self.serialize(sub, q.right) for sub in getattr(ob, k).all()]
                return (shape, k, prop, sub_r)
            elif shape == S.object:
                sub_r = self.serialize(getattr(ob, k), q.right)
                return (shape, k, prop, sub_r)
            else:
                raise NotImplemented(shape)
        else:
            return (S.atom, q, self.control.get_property_from_object(ob, q), getattr(ob, q))

    def add_result(self, r, k, v):
        r[self.renaming_options.get(k, k)] = v

    def build(self, r, shape, q, prop, val):
        if shape == S.atom:
            type_ = self.control.get_type_from_property(prop)
            convert = self.convertions.get(type_)
            if convert:
                self.add_result(r, q, convert(val, r))
            else:
                self.add_result(r, q, val)
        elif shape == S.array:
            self.add_result(r, q, val)
        elif shape == S.object:
            self.add_result(r, q, val)
        else:
            raise NotImplemented(shape)
