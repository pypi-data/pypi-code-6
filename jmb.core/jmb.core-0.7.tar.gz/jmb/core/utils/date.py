from datetime import datetime, time, timedelta

def next_month(d):
    yr, mo = divmod(d.year * 12 + d.month, 12)
    return datetime(yr, mo + 1, 1)

def previous_month(d):
    first_day_this_month = datetime(d.year, d.month, 1)
    last_day = first_day_this_month - timedelta(days=1)
    first_day = datetime(last_day.year, last_day.month, 1)
    return first_day
