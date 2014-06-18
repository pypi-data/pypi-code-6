"""Era date and time tools."""
import calendar
import tzlocal
from pytz import timezone, utc
from datetime import date, datetime, time, timedelta, tzinfo

__all__ = [
    'calendar',
    'date',
    'datetime',
    'daysago',
    'fromts',
    'fromtsms',
    'is_date',
    'is_datetime',
    'is_time',
    'localize',
    'localnow',
    'nextweekday',
    'now',
    'prevweekday',
    'settz',
    'time',
    'timeago',
    'timedelta',
    'timezone',
    'to_datetime',
    'totz',
    'truncate',
    'ts',
    'tsms',
    'tzinfo',
    'tzlocal',
    'weekday',
]

epoch = datetime(1970, 1, 1).replace(tzinfo=utc)
localtz = tzlocal.get_localzone()

mon = 0
tue = 1
wed = 2
thu = 3
fri = 4
sat = 5
sun = 6

second = 1
millisecond = second / 1000.0
microsecond = millisecond / 1000.0
minute = 60 * second
hour = 60 * minute
day = 24 * hour
week = 7 * day
month = 30 * day
year = 365 * day


def is_time(when):
    """Return True if when is a time."""
    return isinstance(when, time)


def is_time_type(cls):
    """Return True if the class is a time type."""
    if not isinstance(cls, type):
        return False
    return issubclass(cls, time)


def is_date(when):
    """Return True if when is a date."""
    return isinstance(when, date) and not isinstance(when, datetime)


def is_date_type(cls):
    """Return True if the class is a date type."""
    if not isinstance(cls, type):
        return False
    return issubclass(cls, date) and not issubclass(cls, datetime)


def is_datetime(when):
    """Return True if when is a datetime."""
    return isinstance(when, datetime)


def is_datetime_type(cls):
    """Return True if the class is a date type."""
    if not isinstance(cls, type):
        return False
    return issubclass(cls, datetime)


def to_datetime(when):
    """
    Convert a date or time to a datetime. If when is a date then it sets the time to midnight. If
    when is a time it sets the date to the epoch. If when is None or a datetime it returns when.
    Otherwise a TypeError is raised. Returned datetimes have tzinfo set to None unless when is a
    datetime with tzinfo set in which case it remains the same.
    """
    if when is None or is_datetime(when):
        return when
    if is_time(when):
        return datetime.combine(epoch.date(), when)
    if is_date(when):
        return datetime.combine(when, time(0))
    raise TypeError("unable to convert {} to datetime".format(when.__class__.__name__))


def settz(when, tz):
    """
    Return the datetime with the timezone set as provided. This forces the timezone to be tz
    without adjusting the time to account for a timezone change.
    """
    if when is None:
        return None
    return to_datetime(when).replace(tzinfo=tz)


def totz(when, tz=None):
    """
    Return a date, time, or datetime converted to a datetime in the given timezone. If when is a
    datetime and has no timezone it is assumed to be local time. Date and time objects are also
    assumed to be UTC. The tz value defaults to UTC. Raise TypeError if when cannot be converted to
    a datetime.
    """
    if when is None:
        return None
    when = to_datetime(when)
    if when.tzinfo is None:
        when = when.replace(tzinfo=localtz)
    return when.astimezone(tz or utc)


def localize(when):
    """Return a value as local time. Shorthand for `era.totz(when, era.localtz)`."""
    return totz(when, localtz)


def now(tz=None):
    """Return the current datetime in the given timezone. The tz value defaults to UTC."""
    return datetime.utcnow().replace(tzinfo=utc)


def localnow():
    """Return the current datetime in local time. Equivelant to `era.now(era.localtz)`."""
    return datetime.now().replace(tzinfo=localtz)


def daysago(days):
    """Return a date so many days ago."""
    return date.today() - timedelta(days=days)


def timeago(tz=None, *args, **kwargs):
    """Return a datetime so much time ago. Takes the same arguments as timedelta()."""
    return totz(datetime.now(), tz) - timedelta(*args, **kwargs)


def ts(when, tz=None):
    """
    Return a Unix timestamp in seconds for the provided datetime. The `totz` function is called
    on the datetime to convert it to the provided timezone. It will be converted to UTC if no
    timezone is provided.
    """
    if not when:
        return None
    when = totz(when, tz)
    return calendar.timegm(when.timetuple())


def tsms(when, tz=None):
    """
    Return a Unix timestamp in milliseconds for the provided datetime. The `totz` function is
    called on the datetime to convert it to the provided timezone. It will be converted to UTC if
    no timezone is provided.
    """
    if not when:
        return None
    when = totz(when, tz)
    return calendar.timegm(when.timetuple()) * 1000 + int(round(when.microsecond / 1000.0))


def fromts(ts, tzin=None, tzout=None):
    """
    Return the datetime representation of the provided Unix timestamp. By defaults the timestamp is
    interpreted as UTC. If tzin is set it will be interpreted as this timestamp instead. By default
    the output datetime will have UTC time. If tzout is set it will be converted in this timezone
    instead.
    """
    if ts is None:
        return None
    when = datetime.utcfromtimestamp(ts).replace(tzinfo=tzin or utc)
    return totz(when, tzout)


def fromtsms(ts, tzin=None, tzout=None):
    """
    Return the Unix timestamp in milliseconds as a datetime object. If tz is set it will be
    converted to the requested timezone otherwise it defaults to UTC.
    """
    if ts is None:
        return None
    when = datetime.utcfromtimestamp(ts / 1000).replace(microsecond=ts % 1000 * 1000)
    when = when.replace(tzinfo=tzin or utc)
    return totz(when, tzout)


def truncate(when, unit, week_start=mon):
    """Return the datetime truncated to the precision of the provided unit."""
    if is_datetime(when):
        if unit == millisecond:
            return when.replace(microsecond=int(when.microsecond / 1000.0) * 1000)
        elif unit == second:
            return when.replace(microsecond=0)
        elif unit == minute:
            return when.replace(second=0, microsecond=0)
        elif unit == hour:
            return when.replace(minute=0, second=0, microsecond=0)
        elif unit == day:
            return when.replace(hour=0, minute=0, second=0, microsecond=0)
        elif unit == week:
            weekday = prevweekday(when, week_start)
            return when.replace(year=weekday.year, month=weekday.month, day=weekday.day,
                                hour=0, minute=0, second=0, microsecond=0)
        elif unit == month:
            return when.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif unit == year:
            return when.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif is_date(when):
        if unit == week:
            return prevweekday(when, week_start)
        elif unit == month:
            return when.replace(day=1)
        elif unit == year:
            return when.replace(month=1, day=1)
    elif is_time(when):
        if unit == millisecond:
            return when.replace(microsecond=int(when.microsecond / 1000.0) * 1000)
        elif unit == second:
            return when.replace(microsecond=0)
        elif unit == minute:
            return when.replace(second=0, microsecond=0)
    return when


def weekday(when, weekday, start=mon):
    """Return the date for the day of this week."""
    if isinstance(when, datetime):
        when = when.date()

    today = when.weekday()
    delta = weekday - today
    if weekday < start and today >= start:
        delta += 7
    elif weekday >= start and today < start:
        delta -= 7
    return when + timedelta(days=delta)


def prevweekday(when, weekday, inclusive=True):
    """
    Return the date for the most recent day of the week. If inclusive is True (the default) today
    may count as the weekday we're looking for.
    """
    if isinstance(when, datetime):
        when = when.date()
    delta = weekday - when.weekday()
    if (inclusive and delta > 0) or (not inclusive and delta >= 0):
        delta -= 7
    return when + timedelta(days=delta)


def nextweekday(when, weekday, inclusive=True):
    """
    Return the date for the next day of the week. If inclusive is True (the default) today may
    count as the weekday we're looking for.
    """
    if isinstance(when, datetime):
        when = when.date()
    delta = weekday - when.weekday()
    if (inclusive and delta < 0) or (not inclusive and delta <= 0):
        delta += 7
    return when + timedelta(days=delta)
