import sys

PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
    integer_types = int,
    text_type = str
else:
    string_types = basestring,
    integer_types = (int, long)
    text_type = unicode


def is_string(value):
    if isinstance(value, string_types):
        return True
    else:
        return False


def is_text(value):
    if isinstance(value, text_type):
        return True
    else:
        return False


def is_integer(value):
    if isinstance(value, integer_types):
        return True
    else:
        return False
