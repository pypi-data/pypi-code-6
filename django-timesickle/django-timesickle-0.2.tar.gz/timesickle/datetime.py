import datetime
import six


try:
    from django.conf import settings
except ImportError:
    pass

"""
A small package that provides a false date to debug with. This can be turned on
and off easily.
"""


__all__ = [
    'dates',
    'now',
    'tomorrow',
    'yesterday',
]


class Dates:
    """
    Based on a dictionary of `date` or `datetime` objects, sets attributes on
    this object. These can also be accesed as in a dictionary.
    """

    def __init__(self, dates):
        self._dates = dates
        for k, v in six.iteritems(dates):
            setattr(self, k, v)

    def __getitem__(self, key):
        return self._dates[key]


try:
    now = lambda: settings.MOCK_NOW
    dates = Dates(settings.SICKLE_DATES)
except NameError:
    # related to settings not being defined
    now = datetime.datetime.now
    dates = Dates({})
