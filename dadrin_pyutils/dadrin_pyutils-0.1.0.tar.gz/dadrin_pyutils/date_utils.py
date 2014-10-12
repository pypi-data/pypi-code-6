from datetime import datetime, date, timedelta as td
from dateutil import parser
__author__ = 'lluiscanet'

def get_dt_between(start_dt, end_dt):
    """
    Get all dates in between start_dt and end_dt

    Args
    :param start_dt: datetime start time
    :param end_dt: datetime start time
    :return: list of dates
    """
    delta = end_dt - start_dt
    dates = [start_dt + td(days=i) for i in range(delta.days + 1)]
    return dates

def get_dates_str_list(dt_format, start_dt_str=None, end_dt_str=None):
    """
    Get a list of strings for dates between start_dt_str and end_dt_str.
    Use yesterday for start_dt_str and end_dt_str by default
    start_dt_str and end_dt_str string in the format 'format'

    Args
    :param start_dt_str: string, datetime start time
    :param end_dt: string, datetime start time
    :return: list of date strings
    """
    if start_dt_str is None and end_dt_str is None:
        yesterday = date.today() - td(1)
        return [yesterday.strftime(dt_format)]

    start_dt = datetime.strptime(start_dt_str, dt_format).date()
    end_dt = datetime.strptime(end_dt_str, dt_format).date()
    return [dt.strftime(dt_format) for dt in get_dt_between(start_dt, end_dt)]

def get_days_ago(num_days):
    """
    Get datetime object of number of dates ago
    :param num_days: int, number of days ago
    :return: datetime of number of days ago
    """
    past = date.today() - td(num_days)
    return parser.parse(past.strftime('%Y-%m-%d'))
