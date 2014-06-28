"""
String to boolean conversion
"""
__all__ = ['convert_bool']


def convert_bool(value):
    """
    Returns the value as a boolean if appropriate

    The value is converted into a boolean if possible. The value will be
    returned unmodified if no suitable conversion found.
    """
    if value.lower() in ('yes', 'true', '1'):
        value = True
    elif value.lower() in ('no', 'false', '0', ''):
        value = False

    return value
