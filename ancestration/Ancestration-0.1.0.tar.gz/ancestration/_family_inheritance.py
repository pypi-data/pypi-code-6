import inspect
import collections
from types import FunctionType

from ancestration import _family_metaclass

from ancestration._errors import (multiple_family_declarations,
    invalid_family_extends, multiple_family_bases,
    different_family_base, no_super_family, no_super_family_base,
    missing_attribute)


families = dict()

is_family = lambda module: module in families


def add_reload_family(module):
    try:
        from imp import reload
    except ImportError:
        pass
    def reload_family():
        del families[module]
        return reload(module)
    module.reload_family = reload_family


class FamilyInheritanceSet(collections.Set):
    __slots__ = ('_set')

    def __init__(self):
        self._set = set()

    def __contains__(self, item):
        return item in self._set

    def __iter__(self):
        return iter(self._set)

    def __len__(self):
        return len(self._set)

    def _add(self, item):
        self._set.add(item)

    def walk(self):
        for child in iter(self._set):
            yield child
            for descendant in child.walk():
                yield descendant


def clone_class(original_cls, module, new_bases=None, new_dct=None):
    name = original_cls.__name__
    if new_bases is None:
        bases = original_cls.__bases__
    else:
        bases = new_bases
    if new_dct is None:
        dct = dict(original_cls.__dict__)
    else:
        dct = new_dct
    new_cls = type(name, bases, dct)
    new_cls.__module__ = module.__name__
    setattr(module, name, new_cls)
    return new_cls


def redefine_function_globals(original_func, new_globals):
    return FunctionType(original_func.__code__, new_globals,
        original_func.__name__)


class FamilyInheritanceItem(FamilyInheritanceSet):
    __slots__ = ('_cls', '_parent', '_family_base', '_super_family_base',
        '_is_inherited', '_name', '_is_base', '_attributes')

    def __init__(self, cls, parent, super_family_base, is_inherited=False):
        FamilyInheritanceSet.__init__(self)
        self._name = cls.__name__
        self._cls = cls
        self._parent = parent
        self._is_inherited = is_inherited
        self._super_family_base = super_family_base
        self._is_base = not isinstance(parent, FamilyInheritanceItem)
        parent._add(self)

    @property
    def name(self):
        return self._name

    @property
    def is_base(self):
        return self._is_base

    @property
    def is_inherited(self):
        return self._is_inherited

    @property
    def cls(self):
        return self._cls

    @property
    def parent(self):
        return self._parent

    @property
    def super_family_base(self):
        return self._super_family_base

    @property
    def attributes(self):
        return self._attributes

    def _replace_class(self, new_cls, module):
        for child in self:
            child._replace_base_class(self._cls, new_cls, module)
        self._is_inherited = False
        self._cls = new_cls

    def _replace_base_class(self, old_base, new_base, module):
        new_bases = tuple(
            new_base if base is old_base else base
            for base in self._cls.__bases__
        )
        new_cls = clone_class(self._cls, module, new_bases)
        for child in self:
            child._replace_base_class(self._cls, new_cls, module)
        self._cls = new_cls

    def __hash__(self):
        return object.__hash__(self)


class FamilyInheritance(collections.Mapping):
    def __init__(self, module, extends):
        if is_family(module):
            raise multiple_family_declarations()
        self._module = module
        self._mapping = dict()
        self._functions = set()
        self._base_classes = FamilyInheritanceSet()
        if extends is None:
            self._super_family = None
        else:
            if not is_family(extends):
                raise invalid_family_extends(extends)
            self._super_family = families[extends]
            # Copy attributes from super family:
            for attr_name in dir(extends):
                if not hasattr(module, attr_name):
                    attr_value = getattr(extends, attr_name)
                    if (attr_value.__class__ is FunctionType and
                            attr_value.__name__ in
                            self._super_family._functions):
                        # Redefine family functions:
                        attr_value = redefine_function_globals(attr_value,
                            module.__dict__)
                        self._functions.add(attr_value.__name__)
                    setattr(module, attr_name, attr_value)
            # Inherit family classes from super family:
            for inherited_item in self._super_family.walk():
                new_bases = []
                if inherited_item.is_base:
                    parent = self._base_classes
                else:
                    parent = self._mapping[inherited_item.parent.name]
                    new_bases.append(parent.cls)
                original_cls = inherited_item.cls
                new_bases.append(original_cls)
                new_bases = tuple(new_bases)
                cls = clone_class(original_cls, module, new_bases, {})
                item = FamilyInheritanceItem(cls, parent, inherited_item,
                    True)
                self._mapping[item.name] = item
        families[module] = self
        add_reload_family(module)

    @property
    def module(self):
        return self._module

    @property
    def super_family(self):
        return self._super_family

    @property
    def base_classes(self):
        return self._base_classes

    def walk(self):
        return self._base_classes.walk()

    def __getitem__(self, key):
        return self._mapping[key]

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._mapping)

    def _compute_bases(self, name, bases):
        # compute super family base:
        try:
            super_family_base = self._super_family[name]
            super_family_base_cls = super_family_base.cls
        except (TypeError, KeyError):
            super_family_base = None
            super_family_base_cls = None
        # compute in-family base and create class bases list:
        new_bases = []
        try:
            family_base = self._mapping[name]
        except KeyError:
            # newly defined family class
            family_base_cls = None
            for base in bases:
                if base.__name__ in self._mapping:
                    if family_base_cls is None:
                        family_base_cls = base
                    else:
                        raise multiple_family_bases()
                elif base is not object and base is not super_family_base_cls:
                    new_bases.append(base)
            if family_base_cls is None:
                family_base = None
            else:
                family_base = self._mapping[family_base_cls.__name__]
        else:
            # redefined family class
            family_base_cls = family_base.cls
            for base in bases:
                try:
                    defined_family_base = self._mapping[base.__name__]
                except KeyError:
                    if (base is not object
                            and base is not super_family_base_cls):
                        new_bases.append(base)
                else:
                    if (defined_family_base is not family_base
                            and base.__name__ != name):
                        raise different_family_base()
        # add family bases to class bases:
        if super_family_base is not None:
            new_bases.insert(0, super_family_base_cls)
        if family_base is not None:
            new_bases.insert(0, family_base_cls)
        if len(new_bases) == 0:
            new_bases.append(object)
        return family_base, super_family_base, tuple(new_bases)

    def _apply_family_inherit(self, name, dct, super_family_base):
        try:
            family_inherit = dct['FAMILY_INHERIT']
        except KeyError:
            return
        if self._super_family is None:
            raise no_super_family()
        if super_family_base is None:
            raise no_super_family_base(name)
        super_family_base_cls = super_family_base.cls
        for family_inherit_name in family_inherit:
            family_inherit_name = str(family_inherit_name)
            try:
                family_inherit_value = getattr(super_family_base_cls,
                    family_inherit_name)
            except AttributeError:
                raise missing_attribute(family_inherit_name)
            dct[family_inherit_name] = family_inherit_value

    def _create_family_class(self, name, bases, dct):
        family_base, super_family_base, new_bases = self._compute_bases(
            name, bases)
        self._apply_family_inherit(name, dct, super_family_base)
        dct['in_family_base'] = None if family_base is None else family_base.cls
        dct['super_family_base'] = (None if super_family_base is None
            else super_family_base.cls)
        cls = _family_metaclass(name, new_bases, dct)
        cls.__module__ = self._module.__name__
        try:
            item = self._mapping[name]
        except KeyError:
            if family_base is None:
                parent_item = self._base_classes
            else:
                parent_item = family_base
            item = FamilyInheritanceItem(cls, parent_item, super_family_base)
            self._mapping[name] = item
        else:
            item._replace_class(cls, self._module)
        return cls

    def _register_family_function(self, func):
        self._functions.add(func.__name__)

del collections