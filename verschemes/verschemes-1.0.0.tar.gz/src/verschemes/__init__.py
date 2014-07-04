# -*- coding: utf-8 -*-
"""verschemes module

This module can be used to manage and enforce rules for version numbering.

"""

import collections as _collections
from functools import total_ordering as _total_ordering
import re as _re

from verschemes._version import __version__, __version_info__


DEFAULT_FIELD_TYPE = int
DEFAULT_SEGMENT_SEPARATOR = '.'


SegmentField = _collections.namedtuple('SegmentField',
                                       'type name re_pattern render')
"""The definition of an atomic portion of a version segment value.

This is an immutable set of metadata defining the parameters of a field in a
`SegmentDefinition`.

The attributes can be set only in the constructor by name or position and can
be accessed by attribute name or item index:

0. :attr:`type` (default: `int`) is the underlying type of the field value.

   Only `int` and `str` have been tested.

1. :attr:`name` (default: "value") is the name of the field, which must be
   unique among all of the fields in a segment.

   Each segment will often have only one field, so the name is defaulted to
   something quite generic, but it must be explicitly set to ensure uniqueness
   when the `SegmentDefinition` contains multiple fields.

2. :attr:`re_pattern` (default: "0|[1-9][0-9]*") is the regular expression
   pattern that the string representation of the field value must match.

3. :attr:`render` (default: `str`) is the function that takes the underlying
   value and returns its appropriate string representation.

"""

SegmentField.__new__.__defaults__ = (DEFAULT_FIELD_TYPE, 'value',
                                     '0|[1-9][0-9]*', str)

DEFAULT_SEGMENT_FIELD = SegmentField()


_SegmentDefinition = _collections.namedtuple('_SegmentDefinition',
    'optional default separator fields')

class SegmentDefinition(_SegmentDefinition):

    """The definition of a version segment.

    This is an immutable set of metadata defining the parameters of a segment.

    The attributes can be set only in the constructor by name or position and
    can be accessed by attribute name or item index:

    0. :attr:`optional` (default: False) indicates whether the segment may be
       excluded from rendering and whether its value is allowed to be
       unspecified even if the segment has no default.

    1. :attr:`default` (default: None) is the implied value of the segment when
       the value is unspecified (or None).

    2. :attr:`separator` (default: '.') is the string within the version's
       string representation that comes just before the segment value(s).

       This value is ignored for the first segment in a version and also not
       rendered when all optional segments before it are unspecified.

    3. :attr:`fields` (default: a singular `SegmentField` instance) is the
       sequence of metadata for the field(s) in the segment.

    """

    # This must be specified again to keep this subclass from making __dict__.
    __slots__ = ()

    def __new__(cls, optional=False, default=None,
                separator=DEFAULT_SEGMENT_SEPARATOR,
                fields=(DEFAULT_SEGMENT_FIELD,)):
        """Provide default values.

        This cannot be done with `__init__` since `self` is immutable.

        """
        if isinstance(fields, SegmentField):
            fields = (fields,)
        elif (not isinstance(fields, tuple) and
              isinstance(fields, _collections.Iterable)):
            fields = tuple(fields)
        if not all([isinstance(x, SegmentField) for x in fields]):
            raise ValueError(
                "Fields must be of type {}.".format(SegmentField))
        if len(set([x.name for x in fields])) < len(fields):
            raise ValueError(
                "Field names must be unique within a segment definition.")
        if default is not None:
            default = cls._validate_value(default, fields)
        return super(SegmentDefinition, cls).__new__(cls, bool(optional),
            default, str(separator), fields)

    @staticmethod
    def _validate_value(value, fields):
        if isinstance(value, str):
            value_string = value
        else:
            values = (list(value)
                      if isinstance(value, _collections.Iterable) else
                      [value])
            if len(values) > len(fields):
                raise ValueError(
                    "More values were given than fields in the segment "
                    "definition.")
            while len(values) < len(fields):
                values.append(None)
            value_string = "".join([x.render(None if y is None else x.type(y))
                                    for x, y in zip(fields, values)])
        re_pattern = '^' + "".join(['(?P<{}>{})'.format(x.name, x.re_pattern)
                                    for x in fields]) + '$'
        match = _re.match(re_pattern, value_string)
        if not match:
            raise ValueError(
                "Version segment {!r} does not match {!r}."
                .format(value_string, re_pattern))
        result = [None if (match.group(fields[i].name) == "" and
                           fields[i].type is not str) else
                  fields[i].type(match.group(fields[i].name))
                  for i in range(len(fields))]
        return result[0] if len(fields) == 1 else tuple(result)

    @property
    def re_pattern(self):
        """The regular expression pattern for the segment's possible string
        representations."""
        return "".join(['(?:{})'.format(x.re_pattern) for x in self.fields])

    def validate_value(self, value):
        """Validate the given value and return the value as the inner type.

        The given value may be a tuple of field values or a string that shall
        be parsed by the fields' regular expressions.

        """
        if value is None:
            if not self.optional and self.default is None:
                raise ValueError(
                    "A value is required because the version segment is not "
                    "optional and has no default.")
            return value
        return self._validate_value(value, self.fields)

    def render(self, value):
        """Return the given segment value as a string."""
        return (self.fields[0].render(value) if len(self.fields) == 1 else
                "".join([self.fields[i].render(value[i])
                         for i in range(len(self.fields))]))

DEFAULT_SEGMENT_DEFINITION = SegmentDefinition()


@_total_ordering
class Version(object):

    """A class whose instances adhere to versioning rules it defines.

    The versioning rules are defined in `SEGMENT_DEFINITIONS`, which may be
    overridden in a subclass to make it more specific to the versioning rules
    represented by the subclass.

    The concept is that the class represents a particular set of versioning
    rules, and the instances of that class are version identifiers that follow
    those rules.

    Pass the constructor either a version identifier as a `str` or the
    individual segment values in order corresponding to the
    `SEGMENT_DEFINITIONS` defined by the class (or any number of integers if
    using the default implementation).  Optional segments and segments with
    default values may be passed a value of `None` or excluded from the end.

    The instance's individual segment values can be accessed or set via
    standard slicing.  For example, ``instance[0]`` returns the value of the
    first segment.

    """

    SEGMENT_DEFINITIONS = ()
    """The parameters for segments in this version.

    If not using the default, this must be set to a sequence of
    `SegmentDefinition`\ s, one for each segment.  This should be done in the
    subclass definition and henceforth remain unmodified (hopefully the CAPs
    hinted at that).  If any changes *are* made after the class has been used,
    they won't be heeded anyway.

    The default (empty sequence) is special in that it allows for a varying and
    infinite number of segments, each following the rules of the default
    `SegmentDefinition`.  This means that the default implementation supports
    the most common versioning structure of an arbitrary number of integer
    segments separated by dots.

    """

    def __init__(self, *values):
        self._values = []
        if len(values) == 1 and isinstance(values[0], str):
            values = values[0]
        self.version = values

    def __repr__(self):
        cls = type(self)
        return ("{}.{}(".format(cls.__module__, cls.__name__) +
                ", ".join([repr(x) for x in self._values]) + ")")

    def __str__(self):
        return self.render()

    def __eq__(self, other):
        if not isinstance(other, Version):
            other_type = type(other)
            try:
                return other_type(self) == other
            except (TypeError, ValueError):
                pass
            try:
                return other_type(str(self)) == other
            # TODO: Manufacture a test case for Python 2 to execute after
            # this point if possible.
            except (TypeError, ValueError):  # pragma: no cover
                pass
            return False  # pragma: no cover
        return self[:] == other[:]

    def __lt__(self, other):
        if not isinstance(other, Version):
            other_type = type(other)
            try:
                return other_type(self) < other
            except (TypeError, ValueError):
                pass
            try:
                return other_type(str(self)) < other
            except (TypeError, ValueError):
                pass
            # When sys.version_info[:2] >= (3, 4) is all that's supported:
            # return NotImplemented
            # Until then, raising this TypeError should be equivalent.
            raise TypeError(
                "unorderable types: {}() < {}()"
                .format(type(self).__name__, other_type.__name__))
        return self[:] < other[:]

    def __getitem__(self, index):
        def get(v, d):
            return v if v is not None else d.default
        definition = self._get_definition_slice(index)
        result = self._values[index]
        if isinstance(index, slice):
            return tuple(map(get, result, definition))
        return get(result, definition)

    def __setitem__(self, index, value):
        def validate(v, d):
            return d.validate_value(v)
        definition = self._get_definition_slice(index, value)
        self._values[index] = (tuple(map(validate, value, definition))
                               if isinstance(index, slice) else
                               validate(value, definition))

    @classmethod
    def _get_definitions(cls):
        result = getattr(cls, '__SEGMENT_DEFINITIONS', None)
        if result is None:
            if not (isinstance(cls.SEGMENT_DEFINITIONS,
                               _collections.Iterable) and
                    all([isinstance(x, SegmentDefinition)
                         for x in cls.SEGMENT_DEFINITIONS])):
                raise TypeError(
                    "SEGMENT_DEFINITIONS for {} is not a sequence of "
                    "SegmentDefinitions."
                    .format(cls))
            result = cls.__SEGMENT_DEFINITIONS = tuple(cls.SEGMENT_DEFINITIONS)
        return result

    @classmethod
    def _get_re(cls):
        result = getattr(cls, '__RE', None)
        if result is None:
            definitions = cls._get_definitions()
            re = ""
            for i in range(len(definitions)):
                d = definitions[i]
                re_segment = ""
                if i > 0:
                    re_segment += "(?:" + _re.escape(d.separator) + ")"
                    if all([x.optional for x in definitions[:i]]):
                        re_segment += "?"
                re_segment += "(?P<segment{}>{})".format(i, d.re_pattern)
                if d.optional:
                    re_segment = "(?:" + re_segment + ")?"
                re += re_segment
            result = cls.__RE = _re.compile('^' + re + '$')
        return result

    def _get_definition_slice(self, index, values=None):
        definitions = self._get_definitions()
        if definitions:
            return definitions[index]
        if values is None:
            values = self._values[index]
        if isinstance(index, slice):
            return (DEFAULT_SEGMENT_DEFINITION,) * len(values)
        return DEFAULT_SEGMENT_DEFINITION

    def _get_version(self):
        return str(self)

    def _set_version(self, value):
        segment_definitions = self._get_definitions()
        if (isinstance(value, str) or
            not isinstance(value, _collections.Iterable)):
            value = str(value)
            if segment_definitions:
                re = self._get_re()
                match = re.match(value)
                if not match:
                    raise ValueError(
                        "Version {!r} does not match {!r}."
                        .format(value, re.pattern))
                value = match.groups()
            else:
                value = value.split(DEFAULT_SEGMENT_SEPARATOR)
        else:
            value = list(value)
            if segment_definitions:
                if len(value) > len(segment_definitions):
                    raise ValueError(
                        "There are too many segment values ({}) for the "
                        "number of segment definitions ({})."
                        .format(len(value), len(segment_definitions)))
                while len(value) < len(segment_definitions):
                    value.append(None)
            elif not value:
                raise ValueError(
                    "One or more values are required when using implicit "
                    "segment definitions.")
        self[:] = value

    version = property(_get_version, _set_version)
    """The version representation.

    This attribute returns the string representation of the version identifier
    (same as passing the instance to `str`) and can also be used to set all of
    the segment values at once with a compatible version string or a sequence
    of values for all non-optional segments.

    """

    def _render_exclude_defaults_callback(self, index, scope=None):
        if scope is None:
            scope = range(len(self._values))
        if index in scope:
            if any([self._values[i] is not None
                    for i in range(index, max(scope) + 1)]):
                return False
        return (self._get_definition_slice(index).optional and
                self._values[index] is None)

    def render(self, exclude_defaults=True, include_callbacks=(),
               exclude_callbacks=()):
        """Render the version into a string representation.

        Pass `False` (or equivalent) for the `exclude_defaults` argument to
        stop the default behavior of excluding optional segments that have a
        default value but have not been explicitly set.

        If there was only one way to render a version, then this method would
        not exist, and its implementation would be in `__str__`.  There is,
        however, only one default way, which is done when `__str__` is called,
        and that is to call this method with its default arguments.

        There could be many ways to render a version, depending on its
        complexity and features.  The base class implements rendering with
        only one simple argument (`exclude_defaults`) and two complex arguments
        (`include_callbacks` and `exclude_callbacks`).  The two complex
        arguments (i.e., callback arguments) allow for future versions and
        subclasses to provide additional simple arguments.  (Keep reading if
        this interests you.)

        The signature of this method should be considered the most volatile in
        the project.  The callback arguments should never be passed by position
        to keep the code prepared for injection of additional simple arguments
        in the base implementation that are more likely to be passed by
        position.

        **Callback structure**

        The callback arguments are sequences of metadata describing how the
        simple arguments are processed.  The metadata may just be a function
        or a sequence consisting of a function and any additional arguments.
        Each callback function requires the 'version' (or 'self' if its a
        method) argument and the 'index' argument.  The "additional" arguments
        mentioned above follow the required arguments in the callback
        function's signature.

        **Callback processing**

        The functions in `include_callbacks` can return `True` (or equivalent)
        to force the segment identified by the 'index' argument to be included
        in the rendering.  If no "include" callbacks force the inclusion of the
        segment, then the functions in `exclude_callbacks` can return `True`
        (or equivalent) to exclude the segment of the version identified by the
        'index' argument in the rendering.  Any segment with a value (i.e., not
        `None`) that is not excluded by this process will be rendered in the
        result.  The `exclude_defaults` argument is an example of a simple
        argument whose affect is implemented via `exclude_callbacks` with the
        `_render_exclude_defaults_callback` method.

        """
        include_callbacks = list(include_callbacks)
        exclude_callbacks = list(exclude_callbacks)
        if exclude_defaults:
            exclude_callbacks.append(self._render_exclude_defaults_callback)

        def callback_affirmative(callback, index):
            args = [index]
            if (not isinstance(callback, _collections.Callable) and
                isinstance(callback, _collections.Iterable)):
                args.extend(callback[1:])
                callback = callback[0]
            return callback(*args)

        result = ""
        definitions = self._get_definition_slice(slice(0, len(self._values)))
        for i in range(len(self._values)):
            definition = definitions[i]
            value = self[i]
            if definition.optional and value is None:
                continue
            include = False
            for callback in include_callbacks:
                if callback_affirmative(callback, i):
                    include = True
            if not include:
                include = True
                for callback in exclude_callbacks:
                    if callback_affirmative(callback, i):
                        include = False
            if not include:
                continue
            if len(result) > 0:
                result += definition.separator
            result += definition.render(value)
        return result
