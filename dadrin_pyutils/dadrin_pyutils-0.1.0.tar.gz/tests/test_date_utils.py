__author__ = 'lluiscanet'

from datetime import datetime, date, timedelta as td
from dateutil import parser
import dadrin_pyutils.date_utils as dtutils
import pytest

dt_format = '%Y-%m-%d'

def test_dates_between():
    start_dt_str = '2014-01-01'
    end_dt_str = '2014-01-05'
    start_dt = datetime.strptime(start_dt_str, dt_format).date()
    end_dt = datetime.strptime(end_dt_str, dt_format).date()
    dates = dtutils.get_dt_between(start_dt, end_dt)
    assert len(dates) == 5
    assert dates == [datetime.strptime('2014-01-01', dt_format).date(),
                     datetime.strptime('2014-01-02', dt_format).date(),
                     datetime.strptime('2014-01-03', dt_format).date(),
                     datetime.strptime('2014-01-04', dt_format).date(),
                     datetime.strptime('2014-01-05', dt_format).date()]

def test_dates_between_one_day():
    dt = '2014-01-01'
    start_dt = datetime.strptime(dt, dt_format).date()
    end_dt = datetime.strptime(dt, dt_format).date()
    dates = dtutils.get_dt_between(start_dt, end_dt)
    assert len(dates) == 1
    assert dates == [datetime.strptime('2014-01-01', dt_format).date()]

def test_dates_between_empty():
    with pytest.raises(TypeError):
        start_dt = datetime.strptime(None, dt_format).date()
        end_dt = datetime.strptime(None, dt_format).date()
        dates = dtutils.get_dt_between(start_dt, end_dt)

def test_dates_between_None():
    with pytest.raises(ValueError):
        start_dt = datetime.strptime('', dt_format).date()
        end_dt = datetime.strptime('', dt_format).date()
        dates = dtutils.get_dt_between(start_dt, end_dt)


def test_dates_str_list():
    start_dt_str = '2014-01-01'
    end_dt_str = '2014-01-05'
    dates = dtutils.get_dates_str_list(dt_format, start_dt_str, end_dt_str)
    assert len(dates) == 5
    assert dates == ['2014-01-01', '2014-01-02', '2014-01-03', '2014-01-04', '2014-01-05']

def test_dates_str_list_one_day():
    dt = '2014-01-01'
    dates = dtutils.get_dates_str_list(dt_format, dt, dt)
    assert len(dates) == 1
    assert dates == ['2014-01-01']

def test_dates_str_list_None():
    yesterday = date.today() - td(1)
    yesterday_str = yesterday.strftime(dt_format)
    dates = dtutils.get_dates_str_list(dt_format, None, None)
    assert len(dates) == 1
    assert dates == [yesterday_str]

def test_dates_str_list_Empty():
    yesterday = date.today() - td(1)
    yesterday_str = yesterday.strftime(dt_format)
    with pytest.raises(ValueError):
        dates = dtutils.get_dates_str_list(dt_format, '', '')
