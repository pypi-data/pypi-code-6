import collections


_transfer_types = {}


def _new_transfer_obj(cls, obj_instance, **kwargs):
    """
    The purpose of this function is to serve as the __new__ method for a
    generated runtime class derived from a collections.namedtuple.

    :param cls: runtime class.
    :param obj_instance: instance of a sqlalchemy class.
    :param kwargs: keyword args to provide values for "extras"
    :return: an immutable data transfer object instance.
    """
    # The parent class invocation takes an expanded tuple of values that should
    # map 1-to-1 in position with the provided attributes.
    vals = ()
    defaults = getattr(cls, "_defaults", {})
    # Need to invoke the superclass tuple with values in order of the parent's
    # namedtuple specification.
    for key in getattr(cls, "_column_keys", []):
        # Default to None if we can't find the key anywhere.
        val = None
        if key in obj_instance.keys():
            # Try for the sqlalchemy class attribute first.
            val = obj_instance[key]
        elif key in getattr(cls, "_extras_keys", []):
            # Try for the "extras" next.
            if key in kwargs.keys():
                # If they gave it to us, use that value.
                val = kwargs.get(key)
            else:
                # Else, try a default.

                default_val = defaults.get(key)
                if default_val is not None:
                    val = default_val
        vals += (val,)

    # This is equivalent to calling "super(Foo, self).fn(*args, **kwargs)"
    # When the class Foo was defined as a class instead of generated.
    _invocation_type = cls.__mro__[0]
    return super(_invocation_type, cls).__new__(_invocation_type, *vals)


def _data_class(sqlalchemy_class, excludes=None, extras=None, name=None,
                mixin=None):
    """
    Generates a runtime class which others will instantiate on a sqlalchemy
    row proxy.

    :param sqlalchemy_class: a sqlalchemy table object.
    :param excludes: array for excluding columns from sqlalchemy_class.
    :param extras: a list (or dict of defaults) of extra attributes.
    :param name: an optional name parameter (mostly for debugging class names).
    :return: a class to instantiate.
    """
    global _transfer_types
    if name is None:
        name = "DataClass_%s" % sqlalchemy_class.name

    # Check if we've already created this class before.
    data_class = _transfer_types.get(name)
    if data_class is not None:
        return data_class

    # Base keys, pulled from the sqlalchemy class.
    _base_keys = [col.name for col in sqlalchemy_class.columns]
    _excludes = excludes or []
    _defaults = {}
    _extras_keys = []
    if extras is not None:
        if isinstance(extras, list):
            _extras_keys = extras
        elif isinstance(extras, dict):
            _extras_keys = extras.keys()
            _defaults = extras

    # remove keys from the set of base keys.
    _base_cols = set.difference(set(_base_keys), set(_excludes))
    _excluded = set.intersection(set(_base_keys), set(_excludes))
    _extras_keys = set.difference(set(_extras_keys), set(_base_cols))
    _extras_keys = set.difference(set(_extras_keys), set(_excludes))
    column_keys = set.union(set(_base_cols), set(_extras_keys))

    tuple_attributes = " ".join(column_keys)
    # The following lines create a generated runtime class.

    # The name of the parent class type will be "anodyne.data.<name>_tuple"
    type_name = "%s_tuple" % name
    data_class_type = collections.namedtuple(type_name, tuple_attributes)

    data_class_dict = dict(
        # How to generate a new instance.
        __new__=_new_transfer_obj,
        # class attributes for internal use and some inspection/debugging.
        _excluded=_excluded,
        _defaults=_defaults,
        _column_keys=column_keys,
        _extras_keys=_extras_keys,
        _table=sqlalchemy_class.fullname,
        # list'd class properties for inspection/debugging.
        extra_keys=lambda self: list(self._extras_keys),
        columns=lambda self: list(self._column_keys),
        excluded_columns=lambda self: list(self._excluded)
    )
    type_classes = (data_class_type,)
    if mixin:
        type_classes += (mixin,)

    data_class = type(
        name,  # The classtype name will be "tincture.transfer.<name>"
        type_classes,  # Inherit from the generated transfer type.
        # This is what eventually updates __dict__ in the class/instance.
        data_class_dict
    )
    # Cache the class by its name, so we don't need to generate it again later.
    _transfer_types[name] = data_class
    return data_class


DataClass = _data_class