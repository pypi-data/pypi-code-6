"""
Core
----

Collection of common functions.

"""
import datetime as dt
import bisect

# Module constants
DAY = dt.timedelta(days=1)
HOUR = dt.timedelta(seconds=60*60)
MIN = dt.timedelta(seconds=60)

def process(date, fmt="%Y%m%d"):
    """convert to dt.datetime object

    :returns: dt.datetime object
    """
    try:
        result = dt.datetime.strptime(date, fmt)
    except TypeError:
        if isinstance(date, dt.datetime):
            result = date
        else:
            raise
    return result

def daterange(start, end=None, fmt="%Y%m%d",
              interval=DAY, numdates=None, todatetime=False):
    """A simple range function over dates

    >>> daterange("20130101", "20130103")
    ["20130101", "20130102", "20130103"]

    :param start: string start date in correct format
    :keyword end: optional end date string
    :keyword fmt: optional datetime format string
    :keyword interval: custom timedelta interval between dates
    :keyword numdates: produces a list of dates of length numdates
    :keyword todatetime: chooses to output results as datetime.datetime objects

    :returns: list of dates
    """
    if end is None:
        end = start
    if numdates is not None:
        end = shiftdate(start, numdates - 1, fmt=fmt,
                        interval=interval)
    dates = []
    start = process(start, fmt)
    end = process(end, fmt)
    now = start
    while (now <= end):
        date = now
        dates.append(date)
        now += interval
    if not todatetime:
        dates = [date.strftime(fmt) for date in dates]
    return dates

def shiftdate(date, days, fmt="%Y%m%d",
              interval=DAY):
    """Shifts a date by a number of days

    >>> shiftdate("20140606", 10)
    "20140616"

    :param date: string representation of a date
    :param days: int number of days to shift by
    :keyword fmt: optional datetime format string

    :returns: string representation of shifted date
    """
    date_dt = dt.datetime.strptime(date, fmt)
    shifted_dt = date_dt + days * interval
    shifted = shifted_dt.strftime(fmt)
    return shifted

def shiftdates(dates, days, fmt="%Y%m%d"):
    """Shifts a list of dates

    Same API as shiftdate, except it operates
    on an iterable of date strings.

    >>> # Shift a list of dates forward 10 days
    >>> shiftdate(["20140606", "20150301"], 10)
    ["20140616", "20150311"]

    :param date: string representation of a date
    :param days: int number of days to shift by
    :keyword fmt: optional datetime format string

    :returns: list of shifted date strings

    .. seealso:: :func:`shiftdate`
    """
    shifted = [shiftdate(date, days, fmt=fmt) for date in dates]
    return shifted

def strptimes(dates, fmt):
    """Maps datetime.strptime onto iterable of strings

    :param dates: list of strings
    :param fmt: datetime.strptime format

    :returns: list of datetime.datetime objects
    """
    return [dt.strptime(item, fmt) for item in dates]

def datewindow(dates, start, end, endpoint=False):
    """Selects indices which satisfy an interval condition

    Chooses dates which lie in the interval [start, end).

    :param dates: list of dates
    :param start: initial date
    :param end: final date
    :option endpoint: flag to include end point in window
    :returns: slice(istart, iend)
    """
    istart = bisect.bisect_left(dates, start)
    if endpoint:
        iend = bisect.bisect_right(dates, end)
    else:
        iend = bisect.bisect_left(dates, end)
    return slice(istart, iend)


def gaps(dates):
    """Finds missing dates within a sequence of dates

    :param dates: list of dates
    :returns: list of missing dates
    """
    result = []
    dates = sorted(dates)
    if len(dates) > 0:
        start = dates[0]
        end = dates[-1]
        for date in daterange(start, end):
            if date not in dates:
                result.append(date)
    return result


def convert(value, infmt, outfmt):
    """converts dates between formats

    Simplifies use of datetime library when intermediate
    datetime object is not required for the use case

    :param value: string representation of date
    :param infmt: input format string
    :param outfmt: output format string
    :returns: correctly formatted date
    """
    return dt.datetime.strptime(value, infmt).strftime(outfmt)
