#!/usr/bin/python

# Copyright: 2014 Dariusz Dwornikowski <dariusz.dwornikowski@cs.put.poznan.pl>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import SOAPpy
from datetime import date, timedelta, datetime
from dateutil import rrule
import calendar
import email
from get_done_date import get_done_date


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def last_day_last_month():
    first_day = date(date.today().year, date.today().month, 1)
    return first_day - timedelta(days=1)

def monthranger(start_date, end_date):
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        last_day = calendar.monthrange(dt.date().year, dt.date().month)[1]
        yield (dt.date() , date(dt.date().year, dt.date().month, last_day))

class RFS(object):

    def __init__(self, obj):
        self.last_modified = date.fromtimestamp(obj.log_modified)
        self.date = date.fromtimestamp(obj.date)
        if obj.pending != 'done':
            self.pending = "pending"
            self.dust = abs(date.today() - self.last_modified).days
            self.done_date = None
        else:
            self.pending = "done"
            self.done_date = get_done_date(obj.bug_num)
            self.rfs = abs(self.date - self.done_date).days
            self.dust = abs(self.date - self.last_modified).days
        self.age = abs(date.today() - self.date).days
        self.subject = obj.subject
        self.bug_number = obj.bug_num

    def __str__(self):
        return "{} subject: {} age:{} dust:{} ttgs:{} dd{} date{}" \
                .format(self.bug_number, self.subject, self.age, self.dust, self.rfs, self.done_date, self.date)


class RFSStats(object):

    url = 'http://bugs.debian.org/cgi-bin/soap.cgi'
    namespace = 'Debbugs/SOAP'
    server = SOAPpy.SOAPProxy(url, namespace)

    def __init__(self):
        self._buglist = self._get_done()

    def _get_done(self):
        bugi = RFSStats.server.get_bugs("package", "sponsorship-requests", "archive", "both")
        return [RFS(b.value) for b in RFSStats.server.get_status(bugi).item]

    def get_global_mttgs(self, start=date(2012,1,1), end=date.today()):
        ''' day - a day in a month '''
        res = []
        for b in self._buglist:
            if b.status == 'done':
                if b.date >= start and b.date <=end and b.done_date <=end:
                    if b.rfs is not None:
                        res.append(b.rfs)
        if len(res) != 0:
            return float(sum(res) / len(res))
        else:
            return -1

    def _get_day_bugs(self, day):
        bdone, bopen = [], []
        bopened, bclosed = [], []
        for b in self._buglist:
            if b.status == 'done':
                if b.date < day and b.done_date > day:
                    bopen.append(b)
                elif b.date < day and b.done_date < day:
                    bdone.append(b)
                elif b.date == day:
                    bopened.append(b)
                elif b.done_date == day:
                    bclosed.append(b)
            else:
                if b.date <= day:
                    bopen.append(b)
        mttgs = self.get_global_mttgs(day)
        return (bopen, bdone, bopened, bclosed, mttgs)

    def get_opened_by_day(self, day):
        return self._get_day_bugs(day)[2]

    def get_closed_by_day(self, day):
        return self._get_day_bugs(day)[3]

    def get_day_bugs(self, day):
        return self._get_day_bugs(day)

    def day_stats(self, day):
        bopen, bdone, bo, bc, mttgs = self._get_day_bugs(day)
        numopen = len(bopen)
        numdone = len(bdone)
        return (numopen, numdone, len(bo), len(bc), mttgs)

    def get_range_stats(self, start, end):
        res = []
        res.append("date,open,done,opened,closed,mttgs")
        for dat in daterange(start, end):
            (b, d, bo, bc, m) = self.day_stats(dat)
            res.append("{},{},{},{},{},{}".format(dat, b,d,bo,bc,m))
        return res

