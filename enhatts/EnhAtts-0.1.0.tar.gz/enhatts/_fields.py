import collections
from importlib import import_module
from enhatts import FieldPreparationErrors, DeleteField
from tinkerpy import anonymous_class
from inspect import isclass


FieldDefinition = collections.namedtuple('FieldDefinition',
    'field_class attributes')


def _mapping_repr(header, mapping,
        getter=lambda mapping, name: mapping[name]):
    fields_repr = '{' + ', '.join(
            '{}: {}'.format(name, getter(mapping, name))
            for name in mapping
        ) + '}'
    return '{}{}'.format(header, fields_repr)


class Fields(collections.Mapping):
    def __init__(self, cls):
        self._own_field_definitions = dict()
        self._own_field_order = list()
        self._own_field_names = set()
        self._field_class_mapping = dict()
        self._cls = cls
        self._before = dict()

    def _clone(self, cls):
        other = Fields(cls)
        other._own_field_definitions = dict(self._own_field_definitions)
        other._own_field_order = list(self._own_field_order)
        other._own_field_names = set(self._own_field_names)
        other._field_class_mapping = dict(self._field_class_mapping)
        return other

    def _register(self, name, field_class, before, attributes):
        self._own_field_definitions[name] = FieldDefinition(field_class,
            attributes)
        def del_attr(attr_name):
            try:
                delattr(self, attr_name)
            except AttributeError:
                pass
        if before is not None:
            if before not in self._get_field_names():
                raise KeyError(
                    'The field "{}", which the field "{}" should be insert before, does not exist.'.format(
                        name, before))
            self._before[before] = name
        if name not in self._get_field_names():
            self._own_field_order.insert(0, name)
            self._own_field_names.add(name)
        del_attr('_field_names')
        del_attr('_length')
        del_attr('_field_order')

    def _base_fields_iterator(self):
        for base_cls in self._cls.__bases__:
            try:
                base_fields = base_cls.FIELDS
            except AttributeError:
                pass
            else:
                yield base_fields

    def _get_field_definition(self, name):
        try:
            return self._own_field_definitions[name]
        except KeyError:
            for base_fields in self._base_fields_iterator():
                try:
                    return base_fields._get_field_definition(name)
                except KeyError:
                    pass
            raise KeyError(name)

    def _get_lazy_field_class(self, field_class_name):
        def get_field_class(cls):
            module = import_module(cls.__module__)
            return getattr(module, field_class_name)
        for base in self._cls.__mro__:
            try:
                return get_field_class(base)
            except AttributeError:
                pass

    def _get_field_class(self, field_definition):
        field_class, attributes = field_definition
        if isinstance(field_class, str):
            field_class_name = field_class
            field_class = self._get_lazy_field_class(field_class_name)
            if field_class is None or not isclass(field_class):
                raise LookupError(
                    'Could not find a field class named "{}" on the modules of the classes in the method resolution order.'.format(
                        field_class_name))
        if len(attributes) > 0:
            module_name = field_class.__module__
            field_class = anonymous_class(field_class, **attributes)
            field_class.__module__ = module_name
        return field_class

    def __getitem__(self, name):
        try:
            return self._field_class_mapping[name]
        except KeyError:
            field_definition = self._get_field_definition(name)
            field_class = self._get_field_class(field_definition)
            self._field_class_mapping[name] = field_class
            return field_class

    def __contains__(self, name):
        return name in self._get_field_names()

    def __iter__(self):
        return iter(self._get_field_order())

    def __len__(self):
        try:
            return self._length
        except AttributeError:
            self._length = len(self._get_field_names())
            return self._length

    def _update_fields(self):
        field_order = list()
        field_names = set()
        def visit(name):
            field_before = self._before.get(name, None)
            if field_before is not None:
                visit(field_before)
            if name not in field_names:
                field_names.add(name)
                field_order.append(name)
        for base_fields in self._base_fields_iterator():
            for name in base_fields._get_field_order():
                visit(name)
        for name in self._own_field_order:
            visit(name)
        self._field_order = field_order
        self._field_names = field_names

    def _get_field_order(self):
        try:
            return self._field_order
        except AttributeError:
            self._update_fields()
            return self._field_order

    def _get_field_names(self):
        try:
            return self._field_names
        except AttributeError:
            self._update_fields()
            return self._field_names

    def __repr__(self):
        return _mapping_repr('FIELDS on {}: '.format(repr(self._cls)), self)


class FieldValuesProxy(collections.Mapping):
    __slots__ = {'_instance_fields', '_changed_fields', '_deleted_fields',
        '_v_mutable', '_changed_field_names', '_deleted_field_names'}

    def __init__(self, instance_fields):
        self._instance_fields = instance_fields
        self._changed_fields = dict()
        self._deleted_fields = set()
        self._changed_field_names = []
        self._deleted_field_names = []

    def __contains__(self, name):
        return self._instance_fields[name]

    def __getitem__(self, name):
        if name in self._deleted_fields:
            raise KeyError('The field "{}" has been deleted.'.format(name))
        try:
            return self._changed_fields[name]
        except KeyError:
            return self._instance_fields[name]

    def __iter__(self):
        return iter(self._instance_fields)

    def __len__(self):
        return len(self._instance_fields)

    def _set(self, name, value):
        try:
            self._deleted_fields.remove(name)
        except KeyError:
            pass
        else:
            self._deleted_field_names.remove(name)
        if name not in self._changed_fields:
            self._changed_field_names.append(name)
        self._changed_fields[name] = value

    def _delete(self, name):
        self[name]
        try:
            del self._changed_fields[name]
        except KeyError:
            pass
        else:
            self._changed_field_names.remove(name)
        if name not in self._deleted_fields:
            self._deleted_fields.add(name)
            self._deleted_field_names.append(name)

    @property
    def _mutable(self):
        try:
            return self._v_mutable
        except AttributeError:
            mutable = MutableFieldValuesProxy(self._instance_fields,
                self._changed_fields, self._deleted_fields,
                self._changed_field_names, self._deleted_field_names)
            self._v_mutable = mutable
            return mutable

    @property
    def changed(self):
        for name in self._changed_field_names:
            yield name

    @property
    def deleted(self):
        for name in self._deleted_field_names:
            yield name


class MutableFieldValuesProxy(FieldValuesProxy):
    def __init__(self, instance_fields, changed_fields, deleted_fields,
            changed_field_names, deleted_field_names):
        self._instance_fields = instance_fields
        self._changed_fields = changed_fields
        self._deleted_fields = deleted_fields
        self._changed_field_names = changed_field_names
        self._deleted_field_names = deleted_field_names

    __setitem__ = FieldValuesProxy._set
    __delitem__ = FieldValuesProxy._delete

    @property
    def _mutable(self):
        return self


class InstanceFields(collections.MutableMapping):
    __slots__ = {'_fields', '_obj', '_field_instances'}

    def __init__(self, fields, obj):
        self._fields = fields
        self._obj = obj
        self._field_instances = dict()

    def __contains__(self, name):
        return self._fields[name]

    def _get_field_instance(self, name):
        try:
            field_instance = self._field_instances[name]
        except KeyError:
            field_class = self._fields[name]
            field_instance = field_class(self._obj, name)
            self._field_instances[name] = field_instance
        return field_instance

    def __getitem__(self, name):
        return self._get_field_instance(name)

    def __setitem__(self, name, value):
        try:
            self._set_multiple({name: value})
        except FieldPreparationErrors as e:
            raise e[name]

    def __delitem__(self, name):
        self._set_multiple({name: DeleteField})

    def __iter__(self):
        return iter(self._fields)

    def __len__(self):
        return len(self._fields)

    def __repr__(self):
        return _mapping_repr('FIELDS on {}: '.format(repr(self._obj)), self,
            lambda mapping, name: repr(mapping[name]))

    def _before_prepare(self, field_values):
        try:
            before_prepare = self._obj.FIELDS_before_prepare
        except AttributeError:
            pass
        else:
            before_prepare(field_values)

    def _before_modifications(self, field_values_proxy):
        try:
            before_modifications = self._obj.FIELDS_before_modifications
        except AttributeError:
            pass
        else:
            before_modifications(field_values_proxy._mutable)

    def _after_modifications(self, field_values_proxy):
        try:
            after_modifications = self._obj.FIELDS_after_modifications
        except AttributeError:
            pass
        else:
            after_modifications(field_values_proxy)

    def _set_multiple(self, field_values):
        self._before_prepare(field_values)
        field_values_proxy = FieldValuesProxy(self)
        exceptions = {}
        for name in self:
            try:
                value = field_values[name]
            except KeyError:
                pass
            else:
                if value is DeleteField:
                    field_values_proxy._delete(name)
                else:
                    field_instance = self._get_field_instance(name)
                    try:
                        prepared_value = field_instance.prepare(value,
                            field_values_proxy)
                    except Exception as e:
                        exceptions[name] = e
                    else:
                        field_values_proxy._set(name, prepared_value)
        if len(exceptions) > 0:
            raise FieldPreparationErrors(exceptions)
        self._before_modifications(field_values_proxy)
        for name in field_values_proxy.changed:
            field_instance = self._get_field_instance(name)
            field_instance.set(field_values_proxy[name])
        for name in field_values_proxy.deleted:
            field_instance = self._get_field_instance(name)
            field_instance.delete()
        self._after_modifications(field_values_proxy)

del collections