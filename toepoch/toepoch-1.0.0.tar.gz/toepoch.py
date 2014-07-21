import datetime
import time

def toepoch(d,t):

    (year,month,day) = d.split('/')
    year = int(year)
    month = int(month)
    day = int(day)

    (hour,minute,second) = t.split(':')
    hour = int(hour)
    minute = int(minute)
    second = int(second)

    dt = datetime.datetime(year, month, day, hour, minute, day)
    epoch = int(time.mktime(dt.timetuple()))
    return epoch
