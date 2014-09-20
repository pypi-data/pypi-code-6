# -*- coding: UTF-8 -*-
'''\
Ancestration – Family Inheritance for Python
============================================

This project implements the so-called *family inheritance* for Python 2 and 3.
It is based on the doctoral thesis of Patrick Lay "Entwurf eines Objektmodells
für semistrukturierte Daten im Kontext von XML Content Management Systemen"
(Rheinische Friedrich-Wilhelms Universität Bonn, 2006) and is developed as
part of the diploma thesis of Michael Pohl "Architektur und Implementierung
des Objektmodells für ein Web Application Framework" (Rheinische
Friedrich-Wilhelms Universität Bonn, 2013-2014).


.. _family_inheritance:

Family Inheritance
------------------

Family inheritance is a concept in which classes and other attributes are
contained in a structure named *family*. A family (the *child family*) can
extend another family (the *super family*), which works similarily to class
inheritance:

*   All non-class attributes of the super family are made available to the
    child family by copying. All *family functions*, specially decorated
    module-level function, are redefined to use the globals of the child
    family.
*   For each *family class* (i.e. a class included in family inheritance) of
    the super family an empty class with the same name is defined, inheriting
    from the original class in addition to the other bases.

    **All family classes use a breadth-first-search attribute (and method)
    resolution order, instead of the depth-first-search Python normally uses.**
    When a family class is redefined (either by defining it again or by
    redefining an inherited class), it's child family classes are redefined as
    well to use the new class as a base class in exchange for the original one,
    this is propagated through the family inheritance tree.

This library allows to use Python modules as *families* and to make Python
new-style classes *family classes*, to include them in the family inheritance.


.. _define_family:

Defining a Family
^^^^^^^^^^^^^^^^^

A module can be made a *family* by calling :func:`family` in it, preferably as
the first statement (after the necessary import). This function takes a module
as the optional argument ``extends``, which specifies the *super family* of
the calling *child family*, and returns the super family module. On calling
:func:`!family` all attributes of the super family are copied to the new family
module, if they are not yet defined there. All inherited family classes are
newly defined to inherit from the super family base and their in-family base.

You can also retrieve attributes from :func:`!family`: the names of the
attribute values returned specify the family to extend, the last one must be
called. Thus instead of calling ``family('foo.bar')`` to extend the family
``foo.bar`` you can write ``family.foo.bar()``.

Classes and non-lambda functions can be integrated into the family inheritance
by calling :func:`adopt` with them as arguments, thus making the family classes
and family functions. The objects can also be specified as strings, then they
are retrieved as attributes from the module :func:`adopt` is called in.

The following pattern has proven useful for the definition of larger families:

*   The family is a Python package and thus also a module, i.e. a directory
    containing at least the file ``__init__.py``, which contains the module code
    of the package.
*   Related functionality is encapsulated in modules below the family package,
    with the module names beginning with a underscore.
*   :func:`adopt` is used in the family package's ``__init__.py`` after it has
    been made a family by calling :func:`family`.

This way it is apparent that the modules are not to be used individually.


.. _define_family_class:

Defining a Family Class
^^^^^^^^^^^^^^^^^^^^^^^

New-style classes of a family can be made *family classes* by setting their
*metaclass* to :func:`family_class <family_class>` or use the latter as a
class decorator. In addition to inheriting from the extented classes (as
specified on definition of a class), a family class also inherits from the
equally named class of the super family. To force inheriting an attribute from
the the super family base class, assign an iterable of names as the attribute
``FAMILY_INHERIT`` of the family class.

**Important notes:** A family class uses a breadth-first-search for determining
the order of its base classes, as opposed to the depth-first-search Python
normally uses, resulting in a different attribute/method resolution order.
Please also note that making a class a family class makes it have a special
metaclass, even if the class was made a family class by using a decorator. This
metaclass is a subclass of :class:`abc.ABCMeta`, making it possible to use the
:meth:`abc.abstractmethod` decorator and to use abstract classes as
mixin-classes.

A family class may extend only one family class and an arbitrary number of
normal Python classes. Inherited family classes can be overridden by
respecifying them (i.e. defining a class with the same name), then the
inheritance tree is modified so that other inherited or newly defined family
classes, extending this class, use the overridden version.

The bases of family classes are redefined, so that:

*   The first base is the in-family base, if the class has one.
*   If there is a super family, the next base (either second or first) is the
    super family base class, if it has one.
*   After that come all non-family base classes.
*   If there is neither an in-family base, nor a super family base and no
    other bases, the only base is :class:`object`.

Thus on redefinition of a family class you do not have to specify the
in-family base class again, it is automatically made the first base.
Similarily you may specify the in-family base or super family base anywhere in
the list of base classes, they will be moved to the front.

On family classes the attributes ``in_family_base`` and ``super_family_base``
are defined, containing the base class of the class' family or the super family
respectively. In addition there is a function ``reload_family`` defined on
family modules, which must be used instead of the built-in ``reload`` function
on families.

To allow for using the current family module to look up attributes, instead of
the namespace, use :attr:`class_module` as a class descriptor. By using the
descriptor attribute's value, code defined earlier can use overridden classes
or other module attributes. :attr:`class_module` can also be called with a class
or instance as its argument to get its module.


Defining a Family Function
^^^^^^^^^^^^^^^^^^^^^^^^^^

A non-lambda module-level function can be registered by name as a `family
function`, by decorating it with :func:`family_function`. Family functions
are accessible in child families under the same name, but the function's
globals dictionary is redefined to be the child family module's dictionary.
This way the function uses overridden classes or other redefined objects in
the child family.


Example
^^^^^^^

Suppose a family ``family_a`` is defined::

    from ancestration import family, family_class, family_method, adopt, class_module

    family()


    @family_function
    def class_a():
        return ClassA


    @family_class
    class ClassA(object)
        def test(self):
            return False


    class ClassB(ClassA)
        module = class_module

        def class_a(self):
            return class_module(self).ClassA


    class ClassC(ClassA)
        @classmethod
        def class_b(cls):
            return cls.module.ClassB


    adopt(ClassB, 'ClassC')


Then a family ``family_b`` can be defined::

    from ancestration import family

    super_family = family.family_a()


    @family_class
    class ClassA(object)
        def test(self):
            return True


    @family_class
    class ClassC(object) # the in-family base does not have to be specified
        @classmethod
        def super_family(cls):
            return super_family


Accordingly the following would be true:

>>> import family_a, family_b # doctest: +SKIP
>>> family_a.ClassB().test() is False # doctest: +SKIP
True
>>> family_b.ClassB().test() is True # doctest: +SKIP
True
>>> family_b.ClassC().test() is True # doctest: +SKIP
True

>>> (family_a.class_a() is family_a.ClassA and
... family_b.class_a() is family_b.ClassA) # doctest: +SKIP
True

>>> (family_a.ClassB().class_a() is family_a.ClassA and
... family_b.ClassB().class_a() is family_b.ClassA) # doctest: +SKIP
True
>>> (family_a.ClassC.class_b() is family_a.ClassB and
... family_b.ClassB.class_b() is family_b.ClassB) # doctest: +SKIP
True
>>> family_b.ClassC.super_family is family_a # doctest: +SKIP
True

>>> (family_b.ClassC.in_family_base is family_b.ClassB and
... family_b.ClassC.super_family_base is family_a.ClassC) # doctest: +SKIP
True

Defining Family Inheritance
---------------------------

.. function:: family(extends=None)

    Makes the module it was called in a family module. See
    :ref:`family_inheritance` and :ref:`define_family` for more information.

    :param extends: The family module to be the super family or :const:`None`
        to define a root family. If the value is neither a module or
        :const:`None` it is assumed to be the name of the family module,
        which is then imported and used.
    :raises ancestration.FamilyInheritanceError: if there is an error in the
        specification of the family module.
    :raises ImportError: if the super family module was specified by name
        and it could not be found.
    :returns: The super family module.

    You can also retrieve attributes from this function and from the returned
    attribute values and call the last (without arguments) to specify
    ``extends``. Each attribute-retrieval step denotes a module, thus instead
    of calling ``family('foo.bar')`` you can write ``family.foo.bar()``.


.. autoclass:: family_class(*args)

.. autofunction:: family_function

.. autofunction:: adopt

.. attribute:: class_module

    A data-descriptor (use as a class attribute) being a proxy to access
    attributes of the module of a class or instance. An access to the
    descriptor attribute raises an :class:`ImportError` if the class's module
    can not be found. Setting or deleting an attribute of this descriptor on
    an instance is not possible.

    It is also callable, which returns the module of a class or instance's
    class.

    :param cls_or_obj: The class or instance of the class to compute the
        module of.
    :raises AttributeError: on old-style class instances.
    :raises ImportError: if the module cannot be found.
    :returns: The module of the class.


.. attribute:: LAZY_CLS_ATTR

    Provides a way to define a class attribute, shadowed by a descriptor, which
    is lazily evaluated at first access, e.g. after its class has been made a
    family class. Retrieve attributes and items from instances of this class or
    call them, to create another instance. Assign such an instance to a class
    attribute, then on first retrieval of this attribute the value is computed
    and saved for cached retrieval.

    Example:

    >>> class Test(object):
    ...     lazy = LAZY_CLS_ATTR.foo[0]['bar']('world')

    >>> Test.foo = [{'bar': lambda name: 'Hello {}!'.format(name)}]
    >>> print(Test.lazy)
    Hello world!

    A :class:`ValueError` is raised on retrieving items, calling or on
    access to the created class attribute, if no attribute was retrieved first:

    >>> class Test(object):
    ...     lazy = LAZY_CLS_ATTR

    >>> Test.lazy
    Traceback (most recent call last):
      ...
    ValueError: First retrieve an attribute from ancestration.LAZY_CLS_ATTR before assigning to a class attribute.

    >>> class Test(object):
    ...     lazy = LAZY_CLS_ATTR()
    Traceback (most recent call last):
      ...
    ValueError: First retrieve an attribute from ancestration.LAZY_CLS_ATTR before calling.

    >>> class Test(object):
    ...     lazy = LAZY_CLS_ATTR[0]
    Traceback (most recent call last):
      ...
    ValueError: First retrieve an attribute from ancestration.LAZY_CLS_ATTR before retrieving items.


.. autoexception:: FamilyInheritanceError
'''

def _get_calling_module(stack_number=1):
    import inspect
    stack = inspect.stack()
    frame = stack[stack_number][0]
    module = inspect.getmodule(frame)
    del stack, frame
    return module


class _FamilyExtender(object):
    def __init__(self, parent, module_name):
        self._parent = parent
        self._module_name = module_name

    def __getattr__(self, module_name):
        return _FamilyExtender(self, module_name)

    def __call__(self):
        def module_names():
            current = self
            while current is not None:
                yield current._module_name
                current = current._parent
        extends = '.'.join(reversed(list(module_names())))
        return family(extends, 3)


class family(object):
    '''\
    Callable to make current module a family.
    '''
    def __call__(self, extends=None, _stack_number=2):
        if extends is not None:
            import inspect
            if not inspect.ismodule(extends):
                from importlib import import_module
                extends = import_module(str(extends))
        module = _get_calling_module(_stack_number)
        from ancestration._family_inheritance import FamilyInheritance
        FamilyInheritance(module, extends)
        return extends

    def __getattr__(self, module_name):
        return _FamilyExtender(None, module_name)

family = family()


class _family_metaclass_mixin(object):
    def mro(self):
        import logging; logging.warn("mro()")
        bases = type.mro(self)
        cls = bases[0]
        from collections import deque
        pending = deque()
        pending.append(cls)
        bases = deque()
        while len(pending) > 0:
            current = pending.popleft()
            bases.append(current)
            pending.extend(current.__bases__)
        import logging; logging.warn(bases)
        return tuple(bases)

    def __new__(metacls, name, bases, dct):
        import logging; logging.warn("__new__()")
        import pdb; pdb.set_trace()
        cls = type.__new__(metacls, name, bases, dct)
        return cls

    def __init__(self, name, bases, dct):
        import logging; logging.warn("__init__()")
        type.__init__(self, name, bases, dct)

import abc

class _family_metaclass(abc.ABCMeta):
    _abcmeta = abc.ABCMeta

    def mro(self):
        bases = type.mro(self)
        cls = bases[0]
        from collections import deque
        visited = set()
        pending = deque()
        pending.append(cls)
        bases = deque()
        while len(pending) > 0:
            current = pending.popleft()
            if current not in visited:
                visited.add(current)
                bases.append(current)
                pending.extend(current.__bases__)
        return tuple(bases)

    def __new__(metacls, name, bases, dct):
        cls = metacls._abcmeta.__new__(metacls, name, bases, dct)
        return cls

    def __init__(self, name, bases, dct):
        self._abcmeta.__init__(self, name, bases, dct)

del abc


class family_class(_family_metaclass):
    '''\
    To be used as a metaclass or as a class decorator. This includes the class
    in the family inheritance. See :ref:`family_inheritance` and
    :ref:`define_family_class` for more information.

    :param args: Must contain either only the class (if used as a class
        decorator) or the name, the tuple of bases and the dictionary of the
        class to create (if used as a metaclass).
    :raises ancestration.FamilyInheritanceError: if there is an error in the
        specification of the family class.
    :raises ValueError: if the wrong number of arguments is supplied.
    :returns: The family class object.
    '''
    def __new__(metacls, *args):
        if len(args) not in (1, 3):
            raise ValueError(
                'Invalid number of arguments, only 1 or 3 are allowed, got {}: {}'.format(
                    len(args), args))
        module = _get_calling_module(2)
        from ancestration._family_inheritance import families
        try:
            family = families[module]
        except KeyError:
            from ancestration._errors import outside_family
            raise outside_family()
        try:
            name, bases, dct = args
        except ValueError:
            cls = args[0]
            name = cls.__name__
            bases = cls.__bases__
            dct = dict(cls.__dict__)
        dct['_family_module'] = module
        return family._create_family_class(name, bases, dct)


def family_function(func):
    '''\
    A function decorator that registers the name of the decorated non-lambda
    function as a `family function`. This means in child family modules the
    same function is available under the same name, but there it uses the
    child family's dictionary for global lookup. Thus it uses overridden
    classes, functions and so on.

    Note that this only works for functions defined and accessible as
    attributes of the family module, not for methods or nested functions.

    :param func: The function to be made a family function.
    :raises ValueError: if ``func`` is not a function or it is a lambda
        function.
    :raises ancestration.FamilyInheritanceError: if it is not used in a
        family module.
    :returns: ``func``
    '''
    import types
    if (func.__class__ is not types.FunctionType
            or func.__class__.__name__ == '<lambda>'):
        raise ValueError('May only be used on non-lambda functions.')
    module = _get_calling_module(2)
    from ancestration._family_inheritance import families
    try:
        family = families[module]
    except KeyError:
        from ancestration._errors import outside_family
        raise outside_family()
    family._register_family_function(func)
    return func


def adopt(*args, **kargs):
    '''\
    A function which integrates the classes and functions given as arguments
    into the family inheritance, thus making them family classes and family
    functions. The arguments may also be strings, in this case the object is
    looked up in the module which is given in the named argument ``module`` and
    defaults to the current (family) module.

    A callback function may be supplied which is called with each adopted
    object. If the returned value is different from :const:`None` the
    class/function is replaced by this value.

    :param args: The functions and classes to integrate into family inheritance,
        may also be given as strings. If none are given but the ``module``
        argument is specified, all classes and functions of that module are
        adopted.
    :param kargs: The named argument ``callback`` may be given as a function
        with one argument, which is called with each adopted object. The named
        argument ``module`` may be a module or a string denoting a module. If a
        ``module`` string starts with a ``.``, it is resolved starting with the
        module where :func:`!adopt` is called from. To create custom
        adoption-functions using this function, specify the named
        ``stack_depth`` argument with a number denoting the number of calls from
        the module where it is called until :func:`!adopt` is called (a function
        to be called instead of :func:`!adopt`, directly calling should specify
        a ``1``). If the named argument ``include_attributes`` is given and
        either :const:`True` or an iterable of strings, all or the given
        non-class and non-function attributes will also be imported.
    :raises FamilyInheritanceError: if an argument specifies neither a class nor
        function.
    :raises ImportError: If the module given in the argument ``module`` as a
        string could not be imported.
    '''
    family_module = _get_calling_module(2 + kargs.get('stack_depth', 0))
    from inspect import isclass, isfunction, ismodule
    islambda = lambda obj: obj.__class__.__name__ == '<lambda>'
    is_family_item = lambda item: ((isclass(item)
            or (isfunction(item) and not islambda(item)))
        and item.__module__ == module.__name__)
    try:
        module = kargs['module']
    except KeyError:
        module = family_module
    else:
        if not ismodule(module):
            if module[0] == '.':
                module = family_module.__name__ + module
            from importlib import import_module
            try:
                module = import_module(module)
            except Exception as e:
                from ancestration._errors import adoption_import_error
                raise adoption_import_error(family_module, module, e)
    try:
        include_attributes = kargs['include_attributes']
        if include_attributes is not True and include_attributes is not False:
            include_attributes = set(str(attr_name)
                for attr_name in include_attributes)
    except KeyError:
        include_attributes = False
    from ancestration._family_inheritance import families
    try:
        family = families[family_module]
    except KeyError:
        from ancestration._errors import outside_family
        raise outside_family()
    callback = kargs.get('callback', None)
    attributes = {}
    if len(args) == 0 and 'module' in kargs:
        items = []
        for name in dir(module):
            item = getattr(module, name)
            if is_family_item(item):
                items.append(item)
            elif include_attributes is not False:
                if include_attributes is True or name in include_attributes:
                    attributes[name] = item
    else:
        items = args
        if include_attributes is not False:
            if include_attributes is True:
                attribute_names = dir(module)
            else:
                attribute_names = include_attributes
            for name in attribute_names:
                item = getattr(module, name)
                attributes[name] = item
    for item in items:
        try:
            if str(item) == item:
                try:
                    item = getattr(module, item)
                except AttributeError:
                    raise FamilyInheritanceError(
                        'There is no attribute "{}" in module "{}".'.format(item,
                            module.__name__))
        except TypeError:
            pass
        name = item.__name__
        if isclass(item):
            bases = item.__bases__
            dct = dict(item.__dict__)
            family_obj = family._create_family_class(name, bases, dct)
        elif isfunction(item) and not islambda(item):
            family._register_family_function(item)
            family_obj = item
        else:
            from ancestration._errors import invalid_adoption_object
            raise invalid_adoption_object(item)
        setattr(family_module, name, family_obj)
        if callback is not None:
            callback_result = callback(family_obj)
            if callback_result is not None:
                family_obj = callback_result
    for attr_name, attr_value in attributes.items():
        setattr(family_module, attr_name, attr_value)


class class_module(object):
    from importlib import import_module
    _import = staticmethod(import_module)

    def __call__(self, cls_or_obj):
        if cls_or_obj.__class__ is type:
            cls = cls_or_obj
        else:
            cls = cls_or_obj.__class__
        return self.__get__(None, cls)

    def __get__(self, obj, cls):
        return self._import(cls.__module__)

    def __set__(self, obj, value):
        raise AttributeError('Setting is not allowed.')

    def __delete__(self, obj):
        raise AttributeError('Deleting is not allowed.')

class_module = class_module()


class super_descriptor(object):
    def __get__(self, obj, cls):
        return super(cls, obj)

    def __set__(self, obj, value):
        raise AttributeError('Setting is not allowed.')

    def __delete__(self, obj):
        raise AttributeError('Deleting is not allowed.')

super_descriptor = super_descriptor()


class FamilyInheritanceError(Exception):
    '''Raised if there is a problem with the family inheritance.'''
    pass


class LAZY_CLS_ATTR(object):
    __slots__ = '_operation', '_parent', '_value', '_has_value'
    __isabstractmethod__ = False # fix for being detected as an abstract method

    def __init__(self, operation, parent):
        self._operation = operation
        self._parent = parent
        self._has_value = False

    def __getattr__(self, name):
        return self.__class__(lambda current: getattr(current, name), self)

    def __getitem__(self, key):
        if self._parent is None:
            raise ValueError(
                'First retrieve an attribute from ancestration.LAZY_CLS_ATTR before retrieving items.')
        return self.__class__(lambda current: current[key], self)

    def __call__(self, *args, **kargs):
        if self._parent is None:
            raise ValueError(
                'First retrieve an attribute from ancestration.LAZY_CLS_ATTR before calling.')
        return self.__class__(lambda current: current(*args, **kargs), self)

    def __get__(self, obj, cls):
        if self._has_value:
            return self._value
        if self._parent is None:
            raise ValueError(
                'First retrieve an attribute from ancestration.LAZY_CLS_ATTR before assigning to a class attribute.')
        from collections import deque
        operations = deque()
        lazy_obj = self
        while lazy_obj is not None:
            operation = lazy_obj._operation
            if operation is not None:
                operations.appendleft(operation)
            lazy_obj = lazy_obj._parent
        value = cls
        while len(operations) > 0:
            operation = operations.popleft()
            value = operation(value)
        self._value = value
        self._has_value = True
        del self._operation, self._parent
        return value

    def __set__(self, obj, value):
        raise AttributeError('Setting is not allowed.')

    def __delete__(self, obj):
        raise AttributeError('Deleting is not allowed.')


LAZY_CLS_ATTR = LAZY_CLS_ATTR(None, None)
