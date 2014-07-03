#
# Copyright (c) 2009, 2013, 2014
#  Adam Tauno Williams <awilliam@whitemice.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
from datetime import tzinfo, timedelta, datetime
import sqlalchemy
import pytz


class UniversalTimeZone(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)


# <http://stackoverflow.com/questions/414952/sqlalchemy-datetime-timezone>
# <http://blog.abourget.net/2009/4/27/sqlalchemy-and-timezone-support>
class UTCDateTime(sqlalchemy.types.TypeDecorator):
    impl = sqlalchemy.types.DateTime
    type = datetime

    def __init__(self, *arg, **kw):
        sqlalchemy.types.TypeDecorator.__init__(self, *arg, **kw)

    def process_bind_param(self, value, engine):
        '''should fire on "input"'''
        if value is None:
            return None
        elif isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=pytz.UTC)
            else:
                value = value.astimezone(pytz.UTC)
            if value.microsecond:
                value = value.replace(microsecond=0)
        else:
            raise ValueError('Unexpected type provided to UTCDateTime')
        return value

    def process_result_value(self, value, engine):
        '''should fire on "output", taking the value from the database'''
        if (value is None):
            return None
        #return pytz.utc.localize(value)
        if not value.tzinfo:
            return pytz.UTC.localize(value)
        return value
