# -*- coding: UTF-8 -*-
'''\
EnhAtts – Enhanced Attributes
=============================

This project implements *properties on steroids* called "fields" for Python 2
and 3  (tested with CPython 2.7 and 3.3  as well as PyPy 2). It is based on the
"Felder" (german for *fields*) concept of the doctoral thesis of Patrick Lay
"Entwurf eines Objektmodells für semistrukturierte Daten im Kontext von XML
Content Management Systemen" (Rheinische Friedrich-Wilhelms Universität Bonn,
2006) and is developed as part of the diploma thesis of Michael Pohl
"Architektur und Implementierung des Objektmodells für ein Web Application
Framework" (Rheinische Friedrich-Wilhelms Universität Bonn, 2013-2014).


What is a Field?
----------------
A *field* is an attribute on a new-style class called *field container*. A
field has a name and a *field class*, which implements the access to the
attribute and is instantiated once per field container instance with the
field's name. On field containers the attribute ``FIELDS`` is defined allowing
access to the *fields mapping* – an ordered mapping which allows access to the
fields by their name.

The class :class:`Field` defines the *field protocol* and serves as a base
class. :class:`DataField` extends this class and adds basic capabilities for
storing data in the field container as an attribute with the name ``_``
appended by the field's name. :class:`ValueField` in contrast stores the value
in its own instance.

In addition to the usual setting, deleting and getting on container instances,
the field protocol also defines a default value, which is returned on getting
on a class, and preparation, which is called before setting to aquire the
value to set and which may raise an exception if the value is invalid.

Getting an item from the fields mapping on a field container instance returns
the field instance. Setting and deleting items in this mapping is the same as
the according access on the attribute. The fields mapping on a container class
allows only getting, which returns the field instance. Iterating over the
mapping is done in the order of the fields, the other mapping methods
:meth:`keys`, :meth:`values` and meth:`items` also use this order.

Setting the ``FIELDS`` attribute on a field container instance with a
dictionary allows to set multiple fields at once with the values from the
dictionary. First all given values are prepared; if at least one preparation
raises an exception, :class:`FieldPreparationErrors` is raised containing the
exceptions thrown by the preparations. If no preparation fails, all fields are
set to their values.


Defining a Field
----------------
A field is defined on a field container class by using the result of calling
:func:`field` as a class decorator. When the decorator is applied, it creates
the ``FIELDS`` class attribute containing a descriptor for the fields mapping,
if this does not yet exist. The decorator also registers the field on the
mapping by its name and creates another class attribute with the name being
the field's name and containing a descriptor for access to the field. The
order of the fields in the mapping is the order in which the field decorators
appear in the source code (i.e. in the reverse order of definition).

If the supplied field class is not a type object, the argument is used as a
string and the field class to use is determined from the module containing the
implementing class. This way a class extending a field container will use
another field class than the container, if there is an attribute on the
containing module with that name.

:func:`field` allows to specify attributes for the field class, in this case
:func:`tinkerpy.anonymous_class` is used to create an anonymous class based on
the given field class. If no field class is specified, :class:`DataField` is
used as the base class.

To omit creating a string for the field name, you can also retrieve an
attribute from :func:`field`, which is a function creating a field with
the name of the attribute becoming the field's name.


Examples
--------

Field Definition
^^^^^^^^^^^^^^^^

First we define some fields as an anonymous classes and a lazy looked up class
based on :class:`DataField`:

>>> class Data(DataField):
...     description='This is data.'
...
...     def show(self):
...         return str(self.get())
...
>>> @field.number(
...     prepare=lambda self, value, field_values: int(value),
...     DEFAULT=None)
... @field('data', 'Data')
... class Test(object):
...     pass


To retrieve the default values, get the attribute values on the container
class:

>>> Test.number is None
True
>>> Test.data
Traceback (most recent call last):
AttributeError: type object 'Data' has no attribute 'DEFAULT'


To access the field classes, use the fields mapping:

>>> print(Test.FIELDS['data'].description)
This is data.


Field Container Instances
^^^^^^^^^^^^^^^^^^^^^^^^^

On a container instance you can set and get the field values:

>>> test = Test()
>>> test.number
Traceback (most recent call last):
AttributeError: 'Test' object has no attribute '_FIELD_number'
>>> test.number = '1'
>>> test.data = None
>>> test.number == 1 and test.data is None
True


If preparation fails, the value is not set:

>>> test.number = 'a'
Traceback (most recent call last):
ValueError: invalid literal for int() with base 10: 'a'
>>> test.number == 1
True


You can also delete field values:

>>> del test.number
>>> del test.FIELDS['data']
>>> test.number
Traceback (most recent call last):
AttributeError: 'Test' object has no attribute '_FIELD_number'
>>> test.data
Traceback (most recent call last):
AttributeError: 'Test' object has no attribute '_FIELD_data'


Setting :attr:`DeleteField` as the value of a field also deletes the value:

>>> test.number = 1
>>> test.data = 'data'
>>> test.number = DeleteField
>>> test.FIELDS['data'] = DeleteField
>>> test.number
Traceback (most recent call last):
AttributeError: 'Test' object has no attribute '_FIELD_number'
>>> test.data
Traceback (most recent call last):
AttributeError: 'Test' object has no attribute '_FIELD_data'


Existence of a field is different from existence of the field value:

>>> hasattr(test, 'number')
False
>>> 'number' in test.FIELDS
True
>>> test.FIELDS['number']
<UNSET enhatts.<anonymous:enhatts.DataField> object>


The field instances are available on the field container instance's field
mapping:

>>> test.data = 1
>>> test.FIELDS['data'].show()
'1'


Setting Multiple Fields
^^^^^^^^^^^^^^^^^^^^^^^

By assigning a mapping to the container instance's fields mapping, you can set
multiple fields at once if no preparation fails:

>>> test.FIELDS = dict(number='2', data=3)
>>> test.number == 2 and test.data == 3
True
>>> try:
...     test.FIELDS = dict(number='a', data=4)
... except FieldPreparationErrors as e:
...     for field_name, error in e.items():
...         print('{}: {}'.format(field_name, error))
number: invalid literal for int() with base 10: 'a'
>>> test.number == 2 and test.data == 3
True

Using :attr:`DeleteField` field values can also be deleted while setting
multiple fields:

>>> test.FIELDS = dict(number=DeleteField, data=0)
>>> not hasattr(test, 'number') and test.data == 0
True


Field Container Callbacks
^^^^^^^^^^^^^^^^^^^^^^^^^

A field container may define callable attributes (e.g. methods), which are
called while changing fields. :func:`FIELDS_before_prepare` is called before
the fields are prepared with the mapping of field values to set.
:func:`FIELDS_before_modifications` is called just before the fields are set
with a mutable mapping being a view on the field values, which keeps track of
the changes to apply. After the fields have been set
:func:`FIELDS_after_modifications` is called with an immutable mapping being
a view on the field values.


.. function:: .FIELDS_before_prepare(field_values)

    Called before preparing the field values.

    :param field_values: The mutable mapping from field name to field value
        containing an entry for each field to set. Field values being
        :attr:`DeleteField` denote the field to be deleted.


.. function:: .FIELDS_before_modifications(fields_proxy)

    Called before modifying the fields.

    :param fields_proxy: A mutable mapping from field name to field value for
        all fields of the container, but with values being as they will be
        after applying the modifications. Changes (setting or deleting items)
        are not applied to the underlying fields mapping, but are executed
        when the modifications are applied. The attributes ``changed`` and
        ``deleted`` contain iterators over the names of changed or deleted
        fields.


.. function:: .FIELDS_after_modifications(fields_proxy)

    Called after setting the fields with the prepared values.

    :param fields_proxy: An immutable mapping from field name to field value
        for all fields of the container. The attributes ``changed`` and
        ``deleted`` contain iterators over the names of changed or deleted
        fields.


Here's an example field container which prints out information and sets the
field revision on changes:

>>> @field('revision')
... class CallbackTest(Test):
...     def __init__(self, **fields):
...         self.FIELDS = fields
...
...     def FIELDS_before_prepare(self, field_values):
...         print('Before preparation of:')
...         for name in sorted(field_values.keys()):
...             print('  {} = {}'.format(name, repr(field_values[name])))
...
...     def FIELDS_before_modifications(self, fields_proxy):
...         print('Changes:')
...         for name in fields_proxy.changed:
...             print('  {} = {}'.format(name, repr(fields_proxy[name])))
...         print('To delete: {}'.format(', '.join(fields_proxy.deleted)))
...         try:
...             revision = self.revision + 1
...         except AttributeError:
...             revision = 0
...         fields_proxy['revision'] = revision
...
...     def FIELDS_after_modifications(self, fields_proxy):
...         print('Revision: {}'.format(self.revision))

>>> callback_test = CallbackTest(number='1', data=None)
Before preparation of:
  data = None
  number = '1'
Changes:
  number = 1
  data = None
To delete:\x20
Revision: 0

>>> callback_test.FIELDS = dict(number=DeleteField, data='data')
Before preparation of:
  data = 'data'
  number = <enhatts.DeleteField>
Changes:
  data = 'data'
To delete: number
Revision: 1


The callbacks are also executed if only a single field is modified:

>>> try:
...     callback_test.number = None
... except TypeError as e:
...     print('ERROR: Value cannot be converted by int().')
Before preparation of:
  number = None
ERROR: Value cannot be converted by int().

>>> callback_test.number = '2'
Before preparation of:
  number = '2'
Changes:
  number = 2
To delete:\x20
Revision: 2

>>> del callback_test.number
Before preparation of:
  number = <enhatts.DeleteField>
Changes:
To delete: number
Revision: 3


Inheritance
^^^^^^^^^^^

The fields on classes extending field containers are appended to the existing
fields. Fields can also be redefined, which doesn't change the position:

>>> class Data(Data):
...     DEFAULT = False
...
>>> @field('attributes', ValueField, 'data')
... @field('number', DEFAULT=True)
... class Extending(Test):
...     pass
...
>>> len(Extending.FIELDS)
3
>>> for name, field_obj in Extending.FIELDS.items():
...     print('{}: {}'.format(name, field_obj))
...
number: <class 'enhatts.<anonymous:enhatts.DataField>'>
attributes: <class 'enhatts.ValueField'>
data: <class 'enhatts.Data'>
>>> print(repr(Extending.FIELDS))
FIELDS on <class 'enhatts.Extending'>: {number: <class 'enhatts.<anonymous:enhatts.DataField>'>, attributes: <class 'enhatts.ValueField'>, data: <class 'enhatts.Data'>}
>>> Extending.data is False
True
>>> Extending.number is True
True
>>> extending = Extending()
>>> extending.FIELDS = {'attributes': 2, 'data': 3}
>>> print(repr(extending.FIELDS)) #doctest: +ELLIPSIS
FIELDS on <enhatts.Extending object at 0x...>: {number: <UNSET enhatts.<anonymous:enhatts.DataField> object>, attributes: <enhatts.ValueField object: 2>, data: <enhatts.Data object: 3>}

Multiple inheritance works the same. We define a diamond inheritance:

>>> @field('a')
... @field('b')
... class A(object):
...     pass
...
>>> @field('a')
... @field('c')
... class B(A): pass
...
>>> @field('d')
... @field('b')
... class C(A): pass
...
>>> @field('e')
... class D(B, C): pass


This leads to the following field orders:

>>> list(A.FIELDS.keys())
['a', 'b']
>>> list(B.FIELDS.keys())
['a', 'b', 'c']
>>> list(C.FIELDS.keys())
['a', 'b', 'd']
>>> list(D.FIELDS.keys())
['a', 'b', 'c', 'd', 'e']


API
---

.. function:: field(name, _field_class=DataField, _before=None, **attributes)

    Creates a class decorator, which does the following on the class it is
    applied to:

    1.  If it  does not yet exist, it creates the attribute ``FIELDS`` on the
        class containing a descriptor for access to the fields mapping.

    1.  It registers a field with name ``name`` on the fields mapping.  If
        ``attributes`` are given an :func:`tinkerpy.anonymous_class` based on
        ``_field_class`` is used as the field class, otherwise
        ``_field_class`` is used as the field class.

    If ``_field_class`` is not a class object (i.e. not of type
    :class:`type`), it is interpreted as a string. This triggers lazy field
    class lookup, meaning the class to use is taken from the module the
    field container class is defined in.

    :param name: The name of the field.
    :type name: :class:`str`
    :param _field_class: The class to use as a field class or as the base of
        an anonmous field class. If this is not a new-style class, it is used
        as a string value, this triggers lazy field class lookup.
    :param _before: The field the newly defined field should be inserted
        before. If this is :const:`None`, the field will be inserted as the
        first.
    :type _before: :class:`str`
    :param attributes: If values are given, an
        :func:`tinkerpy.anonymous_class` is created with these attributes and
        `_field_class` as the base and used as the field class.
    :returns: A class decorator which creates a field on the class it is
        applied to.

    You can also retrieve attributes from this object (except those from
    :class:`object`) which returns functions calling :func:`field` with
    ``name`` being the retrieved attribute name.

    .. function:: .name(_field_class=DataField, _before=None, **attributes)

        Calls :func:`field` with the function name as the first argument
        ``name`` and the function arguments as the appropriate arguments to
        :func:`field`.


.. autoclass:: Field

.. autoclass:: DataField

.. autoclass:: ValueField

.. autoclass:: FieldPreparationErrors

.. attribute:: DeleteField

    A static value indicating to delete a field value when setting a single or
    multiple fields.

'''
import collections
import sys

class Field(object):
    '''\
    This class defines the field protocol.

    :param container: The field container, this becomes the :attr:`container`
        value.
    :param name: The name of the field, it becomes the :attr:`name` value.

    A field class is instantiated once for each field container instance with
    the field's name and the container as the argument. On access to the field
    the methods defined here are called.

    Getting

        The return value of calling :meth:`default` is returned on getting a
        field's value on a field container class.

        On reading a field's value on a field container instance, the result
        of calling :meth:`get` is returned.


    Setting

        Before setting a field's value, :meth:`prepare` is called. If this
        does not raise an exception, :meth:`set` is called to write the
        field's value.

    Deleting

        :meth:`delete` is called on deletion of a field's value.

    The byte an Unicode string values returned by instances of this class
    return the respective string values of the field value.

    Comparisons compare field values. If there is no field value set, all
    comparisons except ``!=`` return :const:`False`. If the compared value
    also has a :meth:`get` method, the return value is used for comparison,
    otherwise the compared value itself.
    '''
    def __init__(self, container, name):
        self._container = container
        self._name = name

    @property
    def container(self):
        '''\
        The field container instance.
        '''
        return self._container

    @property
    def name(self):
        '''\
        The name of the field. The field is accessible through an attribute of
        this name and under this name in the ``FIELDS`` mapping  on a field
        container class and instance.
        '''
        return self._name

    @classmethod
    def default(cls, container_cls, name):
        '''\
        The default value of the field. This implementation returns the value
        of the attribute ``DEFAULT`` on ``cls`` and thus will raise an
        :class:`AttributeError` if this does not exist.

        :param container_cls: The field container class.
        :param name: The field name.
        :raises AttributeError: if there is no attribute ``DEFAULT`` on
            ``cls``.
        :returns: the value of the attribute ``DEFAULT`` on ``cls``.
        '''
        return cls.DEFAULT

    def prepare(self, value, field_values):
        '''\
        Prepares the ``value`` to set on the field container instance
        and should raise an exception, if ``value`` is not valid.

        :param value: The value to prepare.
        :param field_values: A read-only proxy mapping to the field values,
            returning the current field values shadowed by all yet prepared
            field values. The attributes ``changed`` and ``deleted`` contain
            iterators over the names of changed or deleted fields.
        :raises Exception: if ``value`` is not valid.
        :returns: The prepared value, this implementation returns ``value``
            unchanged.
        '''
        return value

    def set(self, value):
        '''\
        Should set the field's value to ``value`` on the field container
        instance or throw an exception, if the field should not be writeable.

        This implmentation raises an :class:`AttributeError` and does nothing
        else.

        :param value: The value to write.
        :raises AttributeError: in this implementation.
        '''
        raise AttributeError('Writing not allowed.')

    def get(self):
        '''\
        Should return the field's value on the field container instance or
        throw an exception, if the field should not be readable.

        This implmentation raises an :class:`AttributeError` and does nothing
        else.

        :raises AttributeError: in this implementation.
        :returns: should return the field's value.
        '''
        raise AttributeError('Reading not allowed.')

    def delete(self):
        '''\
        Should delete the field's value on the field container instance or
        throw an exception, if the field should not be deleteable.

        This implmentation raises an :class:`AttributeError` and does nothing
        else.

        :raises AttributeError: in this implementation.
        '''
        raise AttributeError('Deletion not allowed.')

    def __repr__(self):
        object_repr = object.__repr__(self)
        object_repr = object_repr[:object_repr.rfind(' at ')] + '>'
        try:
            value = self.get()
        except AttributeError:
            return '<UNSET {}'.format(object_repr[1:])
        else:
            return '{}: {}>'.format(object_repr[:-1], repr(value))

    def _get_cmp_values(self, other):
        value = self.get()
        if hasattr(other, 'get'):
            other_value = other.get()
        else:
            other_value = other
        return value, other_value

    def __eq__(self, other):
        try:
            value, other_value = self._get_cmp_values(other)
        except AttributeError:
            return False
        return value == other_value

    def __ne__(self, other):
        try:
            value, other_value = self._get_cmp_values(other)
        except AttributeError:
            return True
        return value != other_value

    def __lt__(self, other):
        try:
            value, other_value = self._get_cmp_values(other)
        except AttributeError:
            return False
        return value < other_value

    def __le__(self, other):
        try:
            value, other_value = self._get_cmp_values(other)
        except AttributeError:
            return False
        return value <= other_value

    def __gt__(self, other):
        try:
            value, other_value = self._get_cmp_values(other)
        except AttributeError:
            return False
        return value > other_value

    def __ge__(self, other):
        try:
            value, other_value = self._get_cmp_values(other)
        except AttributeError:
            return False
        return value >= other_value

    def __str__(self):
        return str(self.get())

    if sys.version_info[0] > 2:
        def __bytes__(self):
            return bytes(self.get())
    else:
        def __unicode__(self):
            return unicode(self.get())


class DataField(Field):
    '''\
    A readable, writeable and deleteable :class:`Field` implementation, using
    an attribute with name ``_FIELD_`` appended by the field's name on the field
    container instance to store the field's value.
    '''
    def __init__(self, container, name):
        Field.__init__(self, container, name)
        self._attribute_name = '_FIELD_{}'.format(name)

    def set(self, value):
        '''\
        Sets the field's value to ``value`` on the field container instance.

        :param value: The value to write.
        '''
        setattr(self.container, self._attribute_name, value)

    def get(self):
        '''\
        Returns the field's value on the field container instance.

        :raises AttributeError: if the field's value is not set.
        :returns: the field's value.
        '''
        return getattr(self.container, self._attribute_name)

    def delete(self):
        '''\
        Deletes the field's value on the field container instance.

        :raises AttributeError: if the field's value is not set.
        '''
        delattr(self.container, self._attribute_name)


class ValueField(Field):
    '''\
    A readable, writable and deletable :class:`Field` implementation, which
    stores its data in an instance attribute accessible through the property
    :attr:`value`.
    '''
    @property
    def value(self):
        '''\
        The value stored in the field instance.
        '''
        return self._value

    def set(self, value):
        '''\
        Sets the field's value to ``value``.

        :param value: The value to write.
        '''
        self._value = value

    def get(self):
        '''\
        Returns the field's value.

        :raises AttributeError: if the field's value is not set.
        :returns: the field's value.
        '''
        return self._value

    def delete(self):
        '''\
        Deletes the field's value.

        :raises AttributeError: if the field's value is not set.
        '''
        del self._value


class field(object):
    '''\
    Object to create fields.
    '''
    def __call__(self, name, _field_class=DataField, _before=None,
            **attributes):
        name = str(name)
        if _before is not None:
            _before = str(_before)
        def decorator(cls):
            from enhatts._descriptors import FieldDescriptor, fields_descriptor
            fields = fields_descriptor(cls)
            field_class = _field_class
            if not isinstance(field_class, type):
                field_class = str(field_class)
            fields._register(name, field_class, _before, attributes)
            FieldDescriptor(cls, name)
            return cls
        return decorator

    def __getattr__(self, name):
        return lambda _field_class=DataField, _before=None, **attributes: (
            self(name, _field_class, _before, **attributes))

field = field()


class DeleteField(object):
    '''\
    A static value indicating to delete a field value when setting a single or
    multiple fields.
    '''
    def __init__(self):
        self._repr = self._create_repr()

    @classmethod
    def _create_repr(cls):
        return '<{}.{}>'.format(cls.__module__, cls.__name__)

    def __repr__(self):
        return self._repr

    __str__ = __repr__

DeleteField = DeleteField()


class FieldPreparationErrors(Exception, collections.Mapping):
    '''\
    This exception is thrown if preparation of at least one field fails, when
    setting multiple field at once by assigning a mapping to the ``FIELDS``
    attribute on a field container instance.

    This exception is a mapping from field names to the appropriate exception
    objects thrown by the :meth:`Field.prepare` calls.
    '''
    def __init__(self, exceptions):
        message = 'Setting the field{} {} failed.'.format(
            's' if len(exceptions) > 1 else '',
            ', '.join('"{}"'.format(name) for name in exceptions)
            )
        Exception.__init__(self, message)
        self._exceptions = exceptions

    def __getitem__(self, name):
        return self._exceptions[name]

    def __iter__(self):
        return iter(self._exceptions)

    def __len__(self):
        return len(self._exceptions)

    def __hash__(self):
        hash_value = Exception.__hash__(self)
        for name in self._exceptions:
            current_hash = hash(name) ^ hash(self._exceptions[name])
            hash_value = hash_value ^ current_hash
        return hash_value

    def __eq__(self, other):
        return (isinstance(other, FieldPreparationErrors)
            and self.message == other.message
            and self._exceptions == other._exceptions)

del collections, sys