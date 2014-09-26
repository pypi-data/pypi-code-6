from django.utils import six
import types


if six.PY3:
    dict_type = dict
    list_type = list
    tuple_type = tuple
    str_type = str
    unicode_type = str
else:
    dict_type = types.DictType
    list_type = types.ListType
    tuple_type = types.TupleType

    str_type = types.StringType
    unicode_type = types.UnicodeType
