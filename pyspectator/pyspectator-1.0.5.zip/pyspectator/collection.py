from collections import MutableMapping, Container
from datetime import datetime, timedelta


class LimitedTimeTable(MutableMapping, Container):

    def __init__(self, time_span):
        self.__storage = dict()
        self.__time_span = None
        self.time_span = time_span

    @property
    def time_span(self):
        return self.__time_span

    @time_span.setter
    def time_span(self, value):
        if isinstance(value, timedelta):
            self.__time_span = value
        else:
            raise TypeError('Invalid argument\'s value type! Expected for "datetime.timedelta".')

    @property
    def oldest(self):
        value = None
        if self.__len__() > 0:
            value = min(self.__storage.keys())
        return value

    @property
    def newest(self):
        value = None
        if self.__len__() > 0:
            value = max(self.__storage.keys())
        return value

    def __getitem__(self, item):
        return self.__storage.__getitem__(item)

    def __setitem__(self, key, value):
        if not isinstance(key, datetime):
            raise TypeError('Invalid key type! Expected for "datetime.datetime".')
        now = datetime.now()
        if key > now:
            raise ValueError('Can\'t set item from future!')
        oldest = self.oldest
        if (oldest is not None) and (oldest != key):
            longest_time_span = now - oldest
            if longest_time_span >= self.time_span:  # Item is too old for current timetable
                self.__delitem__(oldest)
        return self.__storage.__setitem__(key, value)

    def __delitem__(self, key):
        return self.__storage.__delitem__(key)

    def __len__(self):
        return self.__storage.__len__()

    def __iter__(self):
        return self.__storage.__iter__()

    def __contains__(self, item):
        return self.__storage.__contains__(item)