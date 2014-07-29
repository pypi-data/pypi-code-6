# -*- coding: utf-8 -*-
"""verschemes module

This module can be used to manage and enforce rules for version numbering.

"""

# Support Python 2 & 3.
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from verschemes.future import *

import collections
import inspect
import itertools
import re

from verschemes._version import __version__, __version_info__


__all__ = []


def _is_string(value):
    """Return whether `value` is a string."""
    return isinstance(value, (str, future.native_str))


def _validate_string(value):
    """Validate that the input is a string and return it as str."""
    if _is_string(value):
        return str(value)
    raise TypeError(
        "{!r} is not a string."
        .format(value))


__all__.append('DEFAULT_FIELD_TYPE')
DEFAULT_FIELD_TYPE = int
"""The type used for fields with no type explicitly specified."""


__all__.append('SegmentField')
class SegmentField(collections.namedtuple('_SegmentField',
                                          'type name re_pattern render')):

    """The definition of an atomic portion of a version segment value.

    This is an immutable set of metadata defining the parameters of a field in
    a `SegmentDefinition`.

    The attributes can be set only in the constructor by name or position and
    can be accessed by attribute name (preferred) or item index:

    0. :attr:`type` (default: `int`) is the underlying type of the field value.

       Only `int` and `str` have been tested.

    1. :attr:`name` (default: "value") is the name of the field, which must be
       unique among all of the fields in a segment.

       Each segment will often have only one field, so the name is defaulted to
       something quite generic, but it must be explicitly set to ensure
       uniqueness when the `SegmentDefinition` contains multiple fields.

       If the field name is specified, it must be a valid Python identifier
       that does not start with an underscore.  This field can then be
       identified by this name in the segment value of a `Version` subclass if
       the corresponding segment definition contains multiple fields, because
       the value is a subclass of `~collections.namedtuple` named `Segment`
       that has fields corresponding to the segment definition's fields.

    2. :attr:`re_pattern` (default: "[0-9]+") is the regular expression pattern
       that the string representation of the field value must match.

    3. :attr:`render` (default: `str`) is the function that takes the
       underlying value and returns its appropriate string representation.
       Note that in Python 2 this `str` is from the `future` package and is
       similar to `unicode`.

    """

    def __new__(cls, type=DEFAULT_FIELD_TYPE, name='value',
                re_pattern='[0-9]+', render=str):
        """Provide default values, and validate given values.

        This cannot be done with `__init__` since `self` is immutable.

        """
        # Validate type.
        if not inspect.isclass(type):
            raise TypeError(
                "The 'type' argument must be a class.")

        # Validate name.
        name = _validate_string(name)
        if name.startswith('_'):
            raise ValueError(
                "A field name must not begin with an underscore.")
        if not name.isidentifier():
            raise ValueError(
                "A field name must be a valid identifier.")

        # Validate re_pattern.
        re_pattern = _validate_string(re_pattern)
        re.compile(re_pattern)  # valid regular expression check

        # Validate render.
        if not callable(render):
            raise TypeError(
                "The 'render' argument must be callable.")

        # Call the super method.
        return super().__new__(cls, type, name, re_pattern, render)


__all__.append('DEFAULT_SEGMENT_FIELD')
DEFAULT_SEGMENT_FIELD = SegmentField()
"""The default `SegmentField` instance."""


__all__.append('DEFAULT_SEGMENT_SEPARATOR')
DEFAULT_SEGMENT_SEPARATOR = '.'
"""The separator used for segments with no separator explicitly specified."""


__all__.append('SegmentDefinition')
class SegmentDefinition(collections.namedtuple('_SegmentDefinition',
    'optional default separator fields name separator_re_pattern')):

    """The definition of a version segment.

    This is an immutable set of metadata defining the parameters of a segment.

    The attributes can be set only in the constructor by name or position and
    can be accessed by attribute name (preferred) or item index:

    0. :attr:`optional` (default: `False`) indicates whether the segment may be
       excluded from rendering and whether its value is allowed to be
       unspecified even if the segment has no default.

    1. :attr:`default` (default: `None`) is the implied value of the segment
       when the value is unspecified (or `None`).

    2. :attr:`separator` (default: ".") is the string within the version's
       string representation that comes just before the segment value(s).

       This value is ignored for the first segment in a version and also not
       rendered when all optional segments before it are unspecified.

    3. :attr:`fields` (default: a singular `SegmentField` instance) is the
       sequence of metadata (`SegmentField` instances) for the field(s) in the
       segment.

    4. :attr:`name` (default: `None`) is an optional name for the segment.

       If the segment name is specified, it must be a valid Python identifier
       that does not start with an underscore.  This segment can then be
       identified by this name in the `Version` subclass in which it is used:

       a. The constructor and the `Version.replace` method will accept this
          name as a keyword argument, overriding the positional argument if
          also specified.
       b. There will be a read-only property to access this segment's value if
          the name is not already used in the class, so don't use a name that
          matches an existing attribute like 'render' if you want to use this
          property as an alternative to index access.

    5. :attr:`separator_re_pattern` (default: None) is an optional regular
       expression pattern that matches all allowed input separators.

       If it is set, then a string representation given to the `Version`
       subclass constructor will allow any input matching this regular
       expression as the separator for this segment, but the `separator`
       attribute is the normal form used when rendering the version.

       If it is not set, then the `separator` attribute is the only acceptable
       literal input form in addition to being the normal form.

       This value is ignored for the first segment in a version.

    """

    # This must be specified again to keep this subclass from making __dict__.
    __slots__ = ()

    def __new__(cls, optional=False, default=None,
                separator=DEFAULT_SEGMENT_SEPARATOR,
                fields=(DEFAULT_SEGMENT_FIELD,), name=None,
                separator_re_pattern=None):
        """Provide default values, and validate given values.

        This cannot be done with `__init__` since `self` is immutable.

        """
        # Validate optional.
        optional = bool(optional)

        # Validate fields.
        if isinstance(fields, SegmentField):
            fields = (fields,)
        elif (not isinstance(fields, tuple) and
              isinstance(fields, collections.Iterable)):
            fields = tuple(fields)
        if not all(isinstance(x, SegmentField) for x in fields):
            raise ValueError(
                "Fields must be of type {}.".format(SegmentField))
        if len(set(x.name for x in fields)) < len(fields):
            raise ValueError(
                "Field names must be unique within a segment definition.")

        # Validate default.
        if default is not None:
            default = cls._validate_value(default, fields)

        # Validate separator.
        separator = _validate_string(separator)

        # Validate name.
        if name is not None:
            name = _validate_string(name)
            if name.startswith('_'):
                raise ValueError(
                    "A segment name must not begin with an underscore.")
            if not name.isidentifier():
                raise ValueError(
                    "A segment name must be a valid identifier.")

        # Validate separator_re_pattern.
        if separator_re_pattern is not None:
            separator_re_pattern = _validate_string(separator_re_pattern)
            # Validate that the pattern is a valid regular expression.
            re.compile(separator_re_pattern)

        # Call the super method.
        return super().__new__(cls, optional, default, separator, fields, name,
                               separator_re_pattern)

    @staticmethod
    def _validate_value(value, fields):
        if _is_string(value):
            value_string = value
        else:
            values = (list(value)
                      if isinstance(value, collections.Iterable) else
                      [value])
            if len(values) > len(fields):
                raise ValueError(
                    "More values ({}) were given than fields ({}) in the "
                    "segment definition.  {}"
                    .format(len(values), len(fields), values))
            while len(values) < len(fields):
                values.append(None)
            value_string = "".join(x.render(None if y is None else x.type(y))
                                   for x, y in zip(fields, values))
        re_pattern = '^' + "".join('(?P<{}>{})'.format(x.name, x.re_pattern)
                                   for x in fields) + '$'
        match = re.match(re_pattern, value_string)
        if not match:
            raise ValueError(
                "Version segment {!r} does not match {!r}."
                .format(value_string, re_pattern))
        result = []
        for i in range(len(fields)):
            field = fields[i]
            value, type_ = match.group(field.name), field.type
            try:
                value = type_(value)
            except (TypeError, ValueError):
                value = None
            result.append(value)
        return (result[0] if len(fields) == 1 else
                collections.namedtuple('Segment',
                                       ' '.join(x.name for x in fields)
                                       )(*result))

    @property
    def re_pattern(self):
        """The regular expression pattern for the segment's possible string
        representations.

        This is generated from the `~SegmentField.re_pattern`\s of its
        field(s).

        """
        return "".join('(?:{})'.format(x.re_pattern) for x in self.fields)

    @property
    def required(self):
        """Whether a value for this segment is required.

        It is required if it is not optional and has no default value.

        """
        return not self.optional and self.default is None

    def validate_value(self, value):
        """Validate the given value and return the value as the inner type.

        The given value may be:

        * a field value if there is only one field,
        * a tuple of field values, or
        * a string that shall be parsed by the fields' regular expressions.

        The result will be:

        * a field value if there is only one field or
        * a `Segment` (`~collections.namedtuple` subclass) instance whose
          attributes and values correspond to the fields' names and values.

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
                "".join(self.fields[i].render(value[i])
                        for i in range(len(self.fields))))


__all__.append('DEFAULT_SEGMENT_DEFINITION')
DEFAULT_SEGMENT_DEFINITION = SegmentDefinition()
"""The default `SegmentDefinition` instance."""


class _VersionMeta(type):

    __class_cache = {}

    def __new__(cls, name, bases, dct):
        # Validate and generate metadata for the new class.
        definitions = dct.pop('SEGMENT_DEFINITIONS', None)
        if definitions is None:
            for base in bases:
                try:
                    definitions = base.SEGMENT_DEFINITIONS
                except AttributeError:
                    continue
                break
        if definitions is None:
            raise TypeError(
                "SEGMENT_DEFINITIONS must be defined.")
        definitions = cls.__validate_definitions(definitions)
        regex = cls.__generate_re(definitions)

        # Add properties for segment names.
        names = set(dct) | set(itertools.chain.from_iterable(dir(x)
                                                              for x in bases))
        for i, segment in enumerate(definitions):
            sname = segment.name
            if not sname or sname in names:
                # no name or already defined
                continue
            func = lambda o, i=i: o[i]
            func.__doc__ = "The '{}' segment value.".format(sname)
            dct[sname] = property(func)

        # Keep this class a true tuple with no __dict__ attribute.
        dct['__slots__'] = ()

        # Create the new class.
        result = type.__new__(cls, name, bases, dct)

        # Store the metadata generated above for future access.
        cls.__class_cache[result] = definitions, regex

        # Return the new class.
        return result

    @staticmethod
    def __validate_definitions(definitions):
        if not (isinstance(definitions, collections.Iterable) and
                all(isinstance(x, SegmentDefinition) for x in definitions)):
            raise TypeError(
                "SEGMENT_DEFINITIONS is not a sequence of SegmentDefinitions.")
        names = [x.name for x in definitions if x.name]
        if len(names) != len(set(names)):
            raise ValueError(
                "Segment names must be unique.")
        return tuple(definitions)

    @staticmethod
    def __generate_re(definitions):
        count = len(definitions)
        if not count:
            return
        # Get segment definition data needed to build the regex.
        separators = []  # separator regex by segment number
        segments = []  # segment value regex by segment number
        required = None  # first required segment
        non_optional = None  # first non-optional segment
        for i in range(count):
            d = definitions[i]
            separators.append('' if i == 0 else
                              '(?:{})'.format(d.separator_re_pattern)
                              if d.separator_re_pattern else
                              re.escape(d.separator))
            segments.append('(?P<segment{}>{})'
                            .format(i, d.re_pattern))
            if required is None and d.required:
                required = i
            if non_optional is None and not d.optional:
                non_optional = i
        if required is None:
            if non_optional is None:
                raise ValueError(
                    "All of the segments are optional.")
            required = non_optional
        # Build the regex.
        pattern = ''
        segment = ''
        for i in range(count):
            separator = separators[i]
            if segment:
                if separator:
                    pattern += '(?:' + segment + separator + ')?'
                else:
                    pattern += segment + '?'
            segment = segments[i]
            if i < required:
                continue
            if separator and i > required:
                pattern += '(?:' + separator + segment + ')'
            else:
                pattern += segment
            if not definitions[i].required:
                pattern += '?'
            segment = ''
        return re.compile('^' + pattern + '$')

    @property
    def SEGMENT_DEFINITIONS(cls):
        """The tuple of segment definitions."""
        return cls.__class_cache[cls][0]

    @property
    def REGULAR_EXPRESSION(cls):
        """The compiled regular expression that must be matched."""
        return cls.__class_cache[cls][1]


__all__.append('Version')
@python_2_unicode_compatible
class Version(future.with_metaclass(_VersionMeta, tuple)):

    """A class whose instances adhere to the version scheme it defines.

    The versioning rules are defined in `SEGMENT_DEFINITIONS`, which may be
    overridden in a subclass to make it more specific to the version scheme
    represented by the subclass.

    The concept is that the class represents a particular set of versioning
    rules (i.e., a version scheme), and the instances of that class are version
    identifiers that follow those rules.

    Pass the constructor either a version identifier as a `str` or the
    individual segment values in order corresponding to the
    `SEGMENT_DEFINITIONS` defined by the class (or any number of integers if
    using the default implementation).  Optional segments and segments with
    default values may be passed a value of `None` or excluded from the end.

    As of version 1.1, keyword arguments may also be given to the constructor
    when the keywords match the segments' names.  Any keyword arguments for
    segments also specified positionally will override the positional
    arguments.

    The instance's segment values can be accessed via standard indexing,
    slicing, and keys.  For example, ``instance[0]`` returns the value of the
    instance's first segment, ``instance[3:5]`` returns a tuple containing the
    values of the instance's fourth and fifth segments, and since version 1.1
    ``instance['name']`` returns the value of the segment with name 'name'.

    As of version 1.1, individual segment values can also be accessed via
    properties if the segment was given a name and the name does not conflict
    with an existing attribute of the class.

    The segment values acquired from indexing, slicing, keywords, and
    properties are cooked according to the segment definition (basically
    returning the default if the raw value is `None`).  The raw values can be
    accessed with :meth:`get_raw_item`.

    """

    SEGMENT_DEFINITIONS = ()
    """The parameters for segments in this version.

    This can only be set as a class attribute and is validated/captured during
    class creation, after which it can be read as an attribute of the class.
    It cannot be modified within an existing class.  It cannot be accessed
    directly from an instance.

    If not using the default, this must be set to an iterable of
    `SegmentDefinition`\ s, one element for each segment, at least one of which
    must be non-optional.

    The default (empty sequence) is special in that it allows for a variable
    and logically infinite number of segments, each following the rules of the
    default `SegmentDefinition`.  This means that the default implementation
    supports the most common version scheme of an arbitrary number of integer
    segments separated by dots.

    """

    def __new__(cls, *args, **kwargs):
        segment_definitions = cls.SEGMENT_DEFINITIONS
        if len(args) == 1 and _is_string(args[0]):
            # Process a version string passed as the only argument.
            string = args[0]
            if segment_definitions:
                regex = cls.REGULAR_EXPRESSION
                match = regex.match(string)
                if not match:
                    raise ValueError(
                        "Version string {!r} does not match {!r}."
                        .format(string, regex.pattern))
                args = list(match.groups())
            else:
                args = string.split(DEFAULT_SEGMENT_SEPARATOR)
        else:
            # Validate the given args.
            args = list(args)
            if segment_definitions:
                if len(args) > len(segment_definitions):
                    raise ValueError(
                        "There are too many segment values ({}) for the "
                        "number of segment definitions ({})."
                        .format(len(args), len(segment_definitions)))
                while len(args) < len(segment_definitions):
                    args.append(None)
            elif not args:
                raise ValueError(
                    "One or more values are required when using implicit "
                    "segment definitions.")

        # Process `kwargs` into `args`.
        segment_indices = dict([(segment_definitions[i].name, i)
                                for i in range(len(segment_definitions))
                                if segment_definitions[i].name])
        for k, v in kwargs.items():
            if k not in segment_indices:
                raise KeyError(
                    "There is no segment with name {!r}."
                    .format(k))
            args[segment_indices[k]] = v

        # Validate and transform the values in `args`.
        args = [(segment_definitions[i] if segment_definitions else
                 DEFAULT_SEGMENT_DEFINITION).validate_value(args[i])
                for i in range(len(args))]

        # Instantiate, validate, and return the new object.
        result = super().__new__(cls, args)
        result.validate()
        return result

    def __repr__(self):
        cls = type(self)
        return ("{}.{}(".format(cls.__module__, cls.__name__) +
                ", ".join(repr(x) for x in self) + ")")

    def __str__(self):
        return self.render()

    def __eq__(self, other):
        if not isinstance(other, Version):
            as_other = self._coerce_to_type(type(other))
            return False if as_other is None else (as_other == other)
        return self[:] == other[:]

    def __lt__(self, other):
        if not isinstance(other, Version):
            as_other = self._coerce_to_type(type(other))
            return NotImplemented if as_other is None else (as_other < other)
        return self[:] < other[:]

    def _coerce_to_type(self, type_):
        try:
            return type_(self)
        except (TypeError, ValueError):
            pass
        try:
            return type_(str(self))
        except (TypeError, ValueError):
            pass

    def _get_segment_definition(self, item=None):
        definitions = type(self).SEGMENT_DEFINITIONS
        if definitions:
            if item is not None:
                if _is_string(item):
                    definitions = dict((x.name, x) for x in definitions
                                       if x.name)
                definitions = definitions[item]
            return definitions
        return ((DEFAULT_SEGMENT_DEFINITION,) * len(self.get_raw_item(item))
                if item is None or isinstance(item, slice) else
                DEFAULT_SEGMENT_DEFINITION)

    def get_raw_item(self, item=None):
        """Return the raw segment value (or values if `item` is a slice).

        This is an alternative to :meth:`~object.__getitem__` (i.e., bracket
        item retrieval) and named-segment properties, which cook the value(s)
        according to their segment definition(s).

        """
        if item is None:
            item = slice(0, len(self))
        if _is_string(item):
            for index, definition in enumerate(type(self).SEGMENT_DEFINITIONS):
                if definition.name == item:
                    item = index
                    break
            if _is_string(item):
                raise KeyError(item)
        return super().__getitem__(item)

    def __getitem__(self, item):
        def get(v, d):
            return v if v is not None else d.default
        definition = self._get_segment_definition(item)
        value = self.get_raw_item(item)
        return (tuple(map(get, value, definition))
                if isinstance(item, slice) else
                get(value, definition))

    if future.PY2:  # pragma: no coverage  # pragma: no branch
        def __getslice__(self, i, j):
            return self.__getitem__(slice(i, j))

    def _render_exclude_defaults_callback(self, index, scope=None):
        if scope is None:
            scope = range(len(self))
        if index in scope:
            if any(self.get_raw_item(i) is not None
                   for i in range(index, max(scope) + 1)):
                return False
        return (self._get_segment_definition(index).optional and
                self.get_raw_item(index) is None)

    def render(self, exclude_defaults=True, include_callbacks=(),
               exclude_callbacks=()):
        """Render the version into a string representation of normal form.

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
            exclude_callbacks.append(
                type(self)._render_exclude_defaults_callback)

        def callback_affirmative(callback, index):
            args = [self, index]
            if (not callable(callback) and
                isinstance(callback, collections.Iterable)):
                args.extend(callback[1:])
                callback = callback[0]
            return callback(*args)

        result = ""
        definitions = self._get_segment_definition()
        for i in range(len(self)):
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

    def replace(self, **kwargs):
        """Return a copy of this version with the given segments replaced.

        Each keyword argument can either be an underscore ('_') followed by the
        numeric segment index or the segment name.  Each identified segment is
        replaced with the argument's value.  Segment name arguments take
        precedence over underscore-index arguments.

        """
        values = list(self.get_raw_item())
        for k in list(kwargs):
            if k.startswith('_') and k[1:].isdigit():
                values[int(k[1:])] = kwargs.pop(k)
        return type(self)(*values, **kwargs)

    def validate(self):
        """Override this in subclasses that require intersegment validation.

        Raise an appropriate exception if validation fails.

        """
