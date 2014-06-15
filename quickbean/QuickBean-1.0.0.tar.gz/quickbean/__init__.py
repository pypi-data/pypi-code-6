#
#   Copyright 2014 Olivier Kozak
#
#   This file is part of QuickBean.
#
#   QuickBean is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
#   Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
#   any later version.
#
#   QuickBean is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
#   details.
#
#   You should have received a copy of the GNU Lesser General Public License along with QuickBean.  If not, see
#   <http://www.gnu.org/licenses/>.
#

import json


class AutoInit(object):
    """A decorator used to enhance the given class with an auto-generated initializer.

    To use this decorator, you just have to place it in front of your class :

    >>> from quickbean import AutoInit
    >>>
    >>> @AutoInit('property_', 'other_property')
    ... class TestObject(object):
    ...     pass

    You will get an auto-generated initializer taking all the declared properties :

    >>> test_object = TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ... )
    >>>
    >>> test_object.property_
    'value'
    >>> test_object.other_property
    'otherValue'

    """
    def __init__(self, *properties):
        self.properties = properties

    def __call__(self, bean):
        namespace = {'bean': bean}

        auto_init_decorated_bean_exec_template = '\n'.join([
            'class AutoInitDecoratedBean(bean):',
            '\tdef __init__(self, %s):' % ', '.join(self.properties),
            '\n'.join(['\t\tself.%s = %s' % (property_, property_) for property_ in self.properties]),
        ])

        exec auto_init_decorated_bean_exec_template in namespace

        # noinspection PyPep8Naming
        AutoInitDecoratedBean = namespace['AutoInitDecoratedBean']

        AutoInitDecoratedBean.__name__ = bean.__name__

        return AutoInitDecoratedBean


class AutoBean(object):
    """A decorator used to enhance the given class with an auto-generated equality, representation and JSON encoder.

    To use this decorator, you just have to place it in front of your class :

    >>> from quickbean import AutoBean
    >>>
    >>> @AutoBean()
    ... class TestObject(object):
    ...     def __init__(self, property_, other_property, _hidden_property):
    ...         self.property_ = property_
    ...         self.other_property = other_property
    ...         self._hidden_property = _hidden_property

    This is strictly equivalent as :

    >>> from quickbean import AutoEq, AutoRepr, AutoJson
    >>>
    >>> @AutoEq()
    ... @AutoRepr()
    ... @AutoJson()
    ... class TestObject(object):
    ...     def __init__(self, property_, other_property, _hidden_property):
    ...         self.property_ = property_
    ...         self.other_property = other_property
    ...         self._hidden_property = _hidden_property

    """
    def __init__(self, excludes=None, only_includes=None):
        if excludes and only_includes:
            raise Exception("Cannot use both the 'excludes' and 'only_includes' keywords")

        self.excludes = excludes
        self.only_includes = only_includes

    def __call__(self, bean):
        @AutoEq(excludes=self.excludes, only_includes=self.only_includes)
        @AutoRepr(excludes=self.excludes, only_includes=self.only_includes)
        @AutoJson(excludes=self.excludes, only_includes=self.only_includes)
        class AutoBeanDecoratedBean(bean):
            pass

        AutoBeanDecoratedBean.__name__ = bean.__name__

        return AutoBeanDecoratedBean


class AutoEq(object):
    """A decorator used to enhance the given class with an auto-generated equality.

    To use this decorator, you just have to place it in front of your class :

    >>> from quickbean import AutoEq
    >>>
    >>> @AutoEq()
    ... class TestObject(object):
    ...     def __init__(self, property_, other_property, _hidden_property):
    ...         self.property_ = property_
    ...         self.other_property = other_property
    ...         self._hidden_property = _hidden_property

    You will get an auto-generated equality taking all the properties available from your class :

    >>> test_object = TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     _hidden_property='hiddenValue',
    ... )
    >>>
    >>> test_object == TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     _hidden_property='differentHiddenValue',
    ... )
    True
    >>>
    >>> test_object == TestObject(
    ...     property_='value',
    ...     other_property='differentOtherValue',
    ...     _hidden_property='differentHiddenValue',
    ... )
    False

    An interesting thing to note here is that hidden properties -i.e. properties that begin with an underscore- are not
    taken into account.

    It is also possible to exclude arbitrary properties with the 'excludes' keyword :

    >>> @AutoEq(excludes=['excluded_property'])
    ... class TestObject(object):
    ...     def __init__(self, property_, other_property, excluded_property):
    ...         self.property_ = property_
    ...         self.other_property = other_property
    ...         self.excluded_property = excluded_property
    >>>
    >>> test_object = TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     excluded_property='excludedValue',
    ... )
    >>>
    >>> test_object == TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     excluded_property='differentExcludedValue',
    ... )
    True

    If you prefer, it is even possible to do the opposite, that is to say, specifying the only properties to include
    with the 'only_includes' keyword :

    >>> @AutoEq(only_includes=['property_', 'other_property'])
    ... class TestObject(object):
    ...     def __init__(self, property_, other_property, non_included_property):
    ...         self.property_ = property_
    ...         self.other_property = other_property
    ...         self.non_included_property = non_included_property
    >>>
    >>> test_object = TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     non_included_property='nonIncludedValue',
    ... )
    >>>
    >>> test_object == TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     non_included_property='differentNonIncludedValue',
    ... )
    True

    """
    def __init__(self, excludes=None, only_includes=None):
        if excludes and only_includes:
            raise Exception("Cannot use both the 'excludes' and 'only_includes' keywords")

        self.excludes = excludes
        self.only_includes = only_includes

    def __call__(self, bean):
        def is_property_visible(property_):
            if property_.startswith('_'):
                return False
            if self.excludes and property_ in self.excludes:
                return False
            if self.only_includes and property_ not in self.only_includes:
                return False

            return True

        class AutoEqDecoratedBean(bean):
            def __eq__(self, other):
                visible_properties = {
                    property_: self.__dict__[property_]
                    for property_ in self.__dict__
                    if is_property_visible(property_)
                }
                other_visible_properties = {
                    property_: other.__dict__[property_]
                    for property_ in other.__dict__
                    if is_property_visible(property_)
                }

                return self.__class__ is other.__class__ and visible_properties == other_visible_properties

            def __ne__(self, other):
                return not self.__eq__(other)

        AutoEqDecoratedBean.__name__ = bean.__name__

        return AutoEqDecoratedBean


class AutoRepr(object):
    """A decorator used to enhance the given class with an auto-generated representation.

    To use this decorator, you just have to place it in front of your class :

    >>> from quickbean import AutoRepr
    >>>
    >>> @AutoRepr()
    ... class TestObject(object):
    ...     def __init__(self, property_, other_property, _hidden_property):
    ...         self.property_ = property_
    ...         self.other_property = other_property
    ...         self._hidden_property = _hidden_property

    You will get an auto-generated representation taking all the properties available from your class :

    >>> test_object = TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     _hidden_property='hiddenValue',
    ... )
    >>>
    >>> repr(test_object)
    "TestObject(other_property='otherValue', property_='value')"

    An interesting thing to note here is that hidden properties -i.e. properties that begin with an underscore- are not
    taken into account.

    It is also possible to exclude arbitrary properties with the 'excludes' keyword :

    >>> @AutoRepr(excludes=['excluded_property'])
    ... class TestObject(object):
    ...     def __init__(self, property_, other_property, excluded_property):
    ...         self.property_ = property_
    ...         self.other_property = other_property
    ...         self.excluded_property = excluded_property
    >>>
    >>> test_object = TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     excluded_property='excludedValue',
    ... )
    >>>
    >>> repr(test_object)
    "TestObject(other_property='otherValue', property_='value')"

    If you prefer, it is even possible to do the opposite, that is to say, specifying the only properties to include
    with the 'only_includes' keyword :

    >>> @AutoRepr(only_includes=['property_', 'other_property'])
    ... class TestObject(object):
    ...     def __init__(self, property_, other_property, non_included_property):
    ...         self.property_ = property_
    ...         self.other_property = other_property
    ...         self.non_included_property = non_included_property
    >>>
    >>> test_object = TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     non_included_property='nonIncludedValue',
    ... )
    >>>
    >>> repr(test_object)
    "TestObject(other_property='otherValue', property_='value')"

    """
    def __init__(self, excludes=None, only_includes=None):
        if excludes and only_includes:
            raise Exception("Cannot use both the 'excludes' and 'only_includes' keywords")

        self.excludes = excludes
        self.only_includes = only_includes

    def __call__(self, bean):
        def is_property_visible(property_):
            if property_.startswith('_'):
                return False
            if self.excludes and property_ in self.excludes:
                return False
            if self.only_includes and property_ not in self.only_includes:
                return False

            return True

        class AutoReprDecoratedBean(bean):
            def __repr__(self):
                visible_properties = {
                    property_: self.__dict__[property_]
                    for property_ in self.__dict__
                    if is_property_visible(property_)
                }

                return '%s(%s)' % (self.__class__.__name__, ', '.join([
                    '%s=%r' % (property_, value)
                    for property_, value in sorted(visible_properties.items())
                ]))

        AutoReprDecoratedBean.__name__ = bean.__name__

        return AutoReprDecoratedBean


class AutoJson(object):
    """A decorator used to enhance the given class with an auto-generated JSON encoder.

    To use this decorator, you just have to place it in front of your class :

    >>> from quickbean import AutoJson
    >>>
    >>> @AutoJson()
    ... class TestObject(object):
    ...     def __init__(self, property_, other_property, _hidden_property):
    ...         self.property_ = property_
    ...         self.other_property = other_property
    ...         self._hidden_property = _hidden_property

    You will get an auto-generated JSON encoder taking all the properties available from your class :

    >>> test_object = TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     _hidden_property='hiddenValue',
    ... )
    >>>
    >>> test_object.to_json()
    '{"other_property": "otherValue", "property_": "value"}'

    An interesting thing to note here is that hidden properties -i.e. properties that begin with an underscore- are not
    taken into account.

    It is also possible to exclude arbitrary properties with the 'excludes' keyword :

    >>> @AutoJson(excludes=['excluded_property'])
    ... class TestObject(object):
    ...     def __init__(self, property_, other_property, excluded_property):
    ...         self.property_ = property_
    ...         self.other_property = other_property
    ...         self.excluded_property = excluded_property
    >>>
    >>> test_object = TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     excluded_property='excludedValue',
    ... )
    >>>
    >>> test_object.to_json()
    '{"other_property": "otherValue", "property_": "value"}'

    If you prefer, it is even possible to do the opposite, that is to say, specifying the only properties to include
    with the 'only_includes' keyword :

    >>> @AutoJson(only_includes=['property_', 'other_property'])
    ... class TestObject(object):
    ...     def __init__(self, property_, other_property, non_included_property):
    ...         self.property_ = property_
    ...         self.other_property = other_property
    ...         self.non_included_property = non_included_property
    >>>
    >>> test_object = TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     non_included_property='nonIncludedValue',
    ... )
    >>>
    >>> test_object.to_json()
    '{"other_property": "otherValue", "property_": "value"}'

    This decorator relies on the standard JSON encoder (https://docs.python.org/2/library/json.html). Values are then
    encoded according to this JSON encoder. But sometimes, it may be useful to customize how to encode some particular
    properties. This is done through methods named as the corresponding properties suffixed with '_to_json' :

    >>> @AutoJson()
    ... class TestObject(object):
    ...     def __init__(self, property_, other_property, _hidden_property):
    ...         self.property_ = property_
    ...         self.other_property = other_property
    ...         self._hidden_property = _hidden_property
    ...
    ...     def other_property_to_json(self):
    ...         return '%sForJson' % self.other_property
    >>>
    >>> test_object = TestObject(
    ...     property_='value',
    ...     other_property='otherValue',
    ...     _hidden_property='hiddenValue',
    ... )
    >>>
    >>> test_object.to_json()
    '{"other_property": "otherValueForJson", "property_": "value"}'

    """
    def __init__(self, excludes=None, only_includes=None):
        if excludes and only_includes:
            raise Exception("Cannot use both the 'excludes' and 'only_includes' keywords")

        self.excludes = excludes
        self.only_includes = only_includes

    def __call__(self, bean):
        def is_property_visible(property_):
            if property_.startswith('_'):
                return False
            if self.excludes and property_ in self.excludes:
                return False
            if self.only_includes and property_ not in self.only_includes:
                return False

            return True

        class AutoJsonDecoratedBean(bean):
            def to_json(self):
                # noinspection PyShadowingNames
                def value_to_json(property_, value):
                    if hasattr(self, '%s_to_json' % property_):
                        return getattr(self, '%s_to_json' % property_)()
                    if hasattr(value, 'to_json'):
                        return json.loads(value.to_json())

                    return value

                visible_properties = {
                    property_: self.__dict__[property_]
                    for property_ in self.__dict__
                    if is_property_visible(property_)
                }

                return json.dumps({
                    property_: value_to_json(property_, value)
                    for property_, value in sorted(visible_properties.items())
                })

        AutoJsonDecoratedBean.__name__ = bean.__name__

        return AutoJsonDecoratedBean
