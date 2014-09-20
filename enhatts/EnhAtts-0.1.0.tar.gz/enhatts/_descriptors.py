from enhatts._fields import Fields, InstanceFields


class FieldDescriptor(object):
    __slots__ = {'_name'}

    def __init__(self, cls, name):
        # Requires the FIELDS attribute of `cls` to be `fields_descriptor`.
        self._name = name
        setattr(cls, name, self)

    def __get__(self, obj, cls):
        if obj is None:
            return cls.FIELDS[self._name].default(cls, self._name)
        return obj.FIELDS[self._name].get()

    def __set__(self, obj, value):
        obj.FIELDS[self._name] = value

    def __delete__(self, obj):
        del obj.FIELDS[self._name]


class fields_descriptor(object):
    def __call__(self, cls):
        if 'FIELDS' not in cls.__dict__:
            cls.FIELDS = self
        return cls.FIELDS

    def _get_class_fields(self, cls):
        try:
            fields = cls.__dict__['_CLS_FIELDS']
        except KeyError:
            fields = Fields(cls)
            cls._CLS_FIELDS = fields
        else:
            if fields._cls is not cls:
                fields = fields._clone(cls)
                cls._CLS_FIELDS = fields
        return fields

    def _get_instance_fields(self, obj):
        try:
            return obj._v_OBJ_FIELDS
        except AttributeError:
            class_fields = self._get_class_fields(obj.__class__)
            instance_fields = InstanceFields(class_fields, obj)
            obj._v_OBJ_FIELDS = instance_fields
            return instance_fields

    def __get__(self, obj, cls):
        if obj is None:
            return self._get_class_fields(cls)
        return self._get_instance_fields(obj)

    def __set__(self, obj, value):
        try:
            field_values = dict(value)
        except TypeError:
            raise TypeError('Only mapping types may be assigned.')
        self._get_instance_fields(obj)._set_multiple(field_values)

    def __delete__(self, obj):
        raise AttributeError('Deletion not allowed.')

fields_descriptor = fields_descriptor()