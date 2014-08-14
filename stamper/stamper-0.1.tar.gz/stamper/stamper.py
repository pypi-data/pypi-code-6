
import json
import re
import os.path
from datetime import datetime, date, timedelta
from os import symlink, remove, makedirs
from collections import OrderedDict
from operator import itemgetter
import pygal


STAMPS_FILE = os.path.expanduser('~/.workstamps.json')
CHARTS_DIR = os.path.expanduser('~/.workstamps-charts')
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = '%Y-%m-%d %H:%M'
HOURS_DAY = 8
SECS_DAY = HOURS_DAY * 60 * 60


class Stamper(object):

    def __init__(self, stamps_file=STAMPS_FILE, charts_dir=CHARTS_DIR):
        self.stamps_file = stamps_file
        self.charts_dir = charts_dir
        self.ensure_stamps_file()
        self.ensure_charts_dir()
        self.stamps = []

    def __json_load(self, filename):
        """
        Load the stamps from a file in json format, returning
        the parsed list.
        """
        with open(filename, 'r') as stamps_file:
            try:
                stamps = json.load(stamps_file)
            except ValueError:
                stamps = []
        return stamps

    def remove_duplicates(self):
        """
        Remove duplicated stamps from the stamps list
        """
        stamps = [dict(t) for t in set(
            [tuple(d.items()) for d in self.stamps])]
        self.stamps = stamps

    def ensure_stamps_file(self):
        if not os.path.exists(self.stamps_file):
            with open(self.stamps_file, 'w') as stamps_file:
                stamps_file.write('')

    def ensure_charts_dir(self):
        if not os.path.exists(self.charts_dir):
            makedirs(self.charts_dir)

    def load_stamps(self):
        self.stamps = self.__json_load(self.stamps_file)

    def sort_stamps(self):
        """
        Sort all the stamps by start and end dates
        """
        self.stamps = sorted(self.stamps, key=itemgetter('start', 'end'))

    def save_stamps(self):
        with open(self.stamps_file, 'w') as stamps_file:
            json.dump(self.stamps, stamps_file, indent=4)

    def stamp(self, start, end, customer, action):
        self.stamps.append({
            'start': start,
            'end': end,
            'customer': customer,
            'action': action,
        })

    def last_stamp(self, n=1):
        """
        return the stamp in position -n, that is, starting from the latest one
        and going back N positions in the list of stamps
        """
        if not self.stamps:
            return None
        return self.stamps[-n]

    def worktime(self, start, end):
        worktime = (datetime.strptime(end, DATETIME_FORMAT) -
                    datetime.strptime(start, DATETIME_FORMAT))
        return worktime.seconds

    def validate_filter(self, stamp_filter):
        """
        Validate a given filter. Filters can have the following notation:

        - %Y-%m-%d: Times recorded at a given date

        - %Y-%m-%d--%Y-%m-%d: Times recorded between two dates

        - *%Y-%m-%d: Times recorded up to a  given date

        - %Y-%m-%d*: Times recorded from a given date

        - N...N[d|w|m|y]: Times recorded N...N days/weeks/months/years ago

        Important: all date comparisons are made on datetime objects, using
        00:00 as the time (first second of the given day). This means that
        for range filters, the first day is included, but the second day is not
        """
        filter_from = None
        filter_to = None

        if stamp_filter is None:
            return filter_from, filter_to

        if '--' in stamp_filter:
            filter_from, filter_to = stamp_filter.split('--')
            filter_from = datetime.strptime(filter_from, DATE_FORMAT)
            filter_to = datetime.strptime(filter_to, DATE_FORMAT)

        elif stamp_filter.startswith('*'):
            filter_to = datetime.strptime(stamp_filter, '*'+DATE_FORMAT)
            filter_to = filter_to.replace(hour=0, minute=0, second=0)

        elif stamp_filter.endswith('*'):
            filter_from = datetime.strptime(stamp_filter, DATE_FORMAT+'*')
            filter_from = filter_from.replace(hour=0, minute=0, second=0)

        elif re.search(r'(\d+[dD]{1})', stamp_filter):
            number = int(stamp_filter.lower().replace('d', ''))
            delta = timedelta(days=number)
            filter_from = datetime.today() - delta
            filter_from = filter_from.replace(hour=0, minute=0, second=0)

        elif re.search(r'(\d+[wW]{1})', stamp_filter):
            number = int(stamp_filter.lower().replace('w', '')) * 7
            delta = timedelta(days=number)
            filter_from = datetime.today() - delta
            filter_from = filter_from.replace(hour=0, minute=0, second=0)

        elif re.search(r'(\d+[mM]{1})', stamp_filter):
            number = int(stamp_filter.lower().replace('m', ''))
            past = date.today()
            # start travelling in time, back to N months ago
            for n in range(number):
                past = past.replace(day=1) - timedelta(days=1)
            # Now use the year/month from the past + the current day to set
            # the proper date
            filter_from = datetime(past.year, past.month, date.today().day)

        elif re.search(r'(\d+[yY]{1})', stamp_filter):
            number = int(stamp_filter.lower().replace('y', ''))
            today = date.today()
            filter_from = datetime(today.year - number, today.month, today.day)

        else:
            # maybe they are giving us a fixed date
            try:
                filter_from = datetime.strptime(stamp_filter, DATE_FORMAT)
            except:
                # nothing to be used as a filter, go on, printing a warning
                print('[warning] invalid date filter: ' + stamp_filter)
            else:
                filter_from = filter_from.replace(hour=0, minute=0, second=0)
                filter_to = filter_from + timedelta(days=1)

        return filter_from, filter_to

    @property
    def customers(self):
        customers = []
        for stamp in self.stamps:
            if stamp['customer'] not in customers:
                customers.append(stamp['customer'])
        customers.remove(None)
        return customers

    def totals(self, filter_from=None, filter_to=None):
        totals = {}
        for stamp in self.stamps:
            customer = stamp['customer']
            # customer will be None for "start" stamps, having no end time
            if customer:
                start = datetime.strptime(stamp['start'], DATETIME_FORMAT)
                end = datetime.strptime(stamp['end'], DATETIME_FORMAT)
                if filter_from and start < filter_from:
                    # if there is a filter setting a starting date for the
                    # report and the current stamp is from an earlier date, do
                    # not add it to the totals
                    continue
                if filter_to and start > filter_to:
                    # similar for the end date
                    continue
                if customer not in totals:
                    totals[customer] = 0
                totals[customer] += self.worktime(stamp['start'], stamp['end'])
        return totals

    def details(self, filter_customer=None, filter_from=None, filter_to=None):
        details = OrderedDict()
        totals = OrderedDict()
        total_customer = OrderedDict()
        for stamp in self.stamps:
            customer = stamp['customer']
            if customer:
                if filter_customer and customer != filter_customer:
                    # we are getting the details for only one customer, if this
                    # stamp is not for that customer, simply move on and ignore
                    # it
                    continue
                start = datetime.strptime(stamp['start'], DATETIME_FORMAT)
                start_day = start.strftime('%Y-%m-%d')
                end = datetime.strptime(stamp['end'], DATETIME_FORMAT)
                if filter_from and start < filter_from:
                    # if there is a filter setting a starting date for the
                    # report and the current stamp is from an earlier date, do
                    # not add it to the totals
                    continue
                if filter_to and start > filter_to:
                    # similar for the end date
                    continue
                # avoid "start" stamps
                if start_day not in details:
                    details[start_day] = []
                if start_day not in totals:
                    totals[start_day] = 0
                worktime = self.worktime(stamp['start'], stamp['end'])
                details[start_day].append(
                    '%(worktime)s %(customer)s %(action)s' % {
                        'worktime': str(timedelta(seconds=worktime)),
                        'customer': customer,
                        'action': stamp['action']
                    })
                totals[start_day] += worktime
                if start_day not in total_customer:
                    total_customer[start_day] = {}
                if customer not in total_customer[start_day]:
                    total_customer[start_day][customer] = 0
                total_customer[start_day][customer] += worktime
        for day in totals:
            totals[day] = str(timedelta(seconds=totals[day]))
        return details, totals, total_customer

    def timeline(self, customer=None, stamp_filter=None):
        filter_from, filter_to = self.validate_filter(stamp_filter)
        for stamp in self.stamps:
            start = datetime.strptime(stamp['start'], DATETIME_FORMAT)
            start_day = start.strftime('%Y-%m-%d')
            if filter_from and start < filter_from:
                # if there is a filter setting a starting date for the
                # report and the current stamp is from an earlier date, do
                # not add it to the totals
                continue
            if filter_to and start > filter_to:
                # similar for the end date
                continue

            if not stamp['customer']:
                if customer is None:
                    print(stamp['start'] + ' start')
            else:
                if customer and customer != stamp['customer']:
                    continue
                if customer:
                    print(stamp['start'] + ' start')
                print(' '.join([stamp['end'],
                                stamp['customer'],
                                stamp['action']]))

    def graph_stamps(self, customer=None, stamp_filter=None):
        """
        Generate charts with information from the stamps
        """
        filter_from, filter_to = self.validate_filter(stamp_filter)
        chart = pygal.Bar(title='Work hours per day',
                          range=(0, HOURS_DAY),
                          x_title='Days',
                          y_title='Work hours',
                          x_label_rotation=45)

        details, totals, totals_customers = self.details(customer,
                                                         filter_from,
                                                         filter_to)
        days = []
        values = {}
        for c in self.customers:
            values[c] = []

        found = []

        for day in details:
            for c in values:
                seconds = totals_customers[day].get(c, 0)
                if seconds and c not in found:
                    found.append(c)
                human = timedelta(seconds=seconds).__str__()
                values[c].append({'value': seconds/60.00/60.00,
                                  'label': day + ': ' + human})
            days.append(day)
        chart.x_labels = map(str, days)

        if customer:
            chart.add(customer, values[customer])
        else:
            for c in found:
                chart.add(c, values[c])

        chart_name = 'chart-%s.svg' % datetime.today().strftime(
            '%Y-%m-%d_%H%M%S')
        chart_symlink = 'chart-latest.svg'
        chart_path = os.path.join(self.charts_dir, chart_name)
        chart_symlink_path = os.path.join(self.charts_dir, chart_symlink)

        chart.render_to_file(chart_path)
        print('Rendered chart: ' + chart_path)
        if os.path.islink(chart_symlink_path):
            remove(chart_symlink_path)
        symlink(chart_name, chart_symlink_path)
        print('Updated latest chart: ' + chart_symlink_path)

    def show_stamps(self, customer=None, stamp_filter=None, verbose=False,
        sum=False):
        filter_from, filter_to = self.validate_filter(stamp_filter)

        # If the user asks for verbose information, show it before the
        # totals (mimicing what the original stamp tool does)
        if verbose:
            details, totals, total_customer = self.details(customer,
                                                           filter_from,
                                                           filter_to)
            for day in details:
                print('------ %(day)s ------' % {'day': day})
                for line in details[day]:
                    print(line)
                customer_day_totals = []
                for tc in total_customer[day]:
                    tc_total = str(timedelta(seconds=total_customer[day][tc]))
                    customer_day_totals.append(tc+': '+tc_total)
                print(', '.join(customer_day_totals))
                if len(customer_day_totals) > 1:
                    # if there are multiple customers in the report, show the
                    # daily totals
                    print('daily total: %(total)s' % {'total': totals[day]})
            print '-'*79

        # now calculate the totals and show them
        totals = self.totals(filter_from, filter_to)
        if customer:
            seconds=totals.get(customer, 0)
            total = timedelta(seconds=totals.get(customer, 0))
            print(' %(customer)s: %(total)s' % {'customer': customer,
                                                'total': total})
        else:
            for c in totals:
                seconds=totals[c]
                total = timedelta(seconds=totals[c])
                print(' %(customer)s: %(total)s' % {'customer': c,
                                                    'total': total})

        if sum:
            sum_tot = ''
            if totals:
                print('------ Totals ------' % {'day': day})
                for day, tot in totals.iteritems():
                    print(' %(day)s: %(total)s' % {'day': day, 'total': tot})
                    sum_tot = "%(total)s %(new)s" % {
                        'total': sum_tot,
                        'new': total
                    }
                totalSecs, sec = divmod(seconds, 60)
                hr, min = divmod(totalSecs, 60)
                totalDays, remaining = divmod(seconds, SECS_DAY)
                remainingMin, remainingSec = divmod(remaining, (60))
                remainingHr, remainingMin = divmod(remainingMin, (60))
                print('----- %d:%02d:%02d -----' % (hr, min, sec))
                print('--- %d days, remaining: %d:%02d (%d hours/day) ---' % (
                    totalDays, remainingHr, remainingMin, HOURS_DAY
                ))

    def remove_stamps(self, n=1):
        """
        Remove up to n stamps back, asking for confirmation before delete
        """
        for i in range(n):
            stamp = self.last_stamp()
            if not stamp['customer']:
                print(stamp['start'] + ' start')
            else:
                print(' '.join([stamp['end'],
                                stamp['customer'],
                                stamp['action']]))
            confirm = ''
            while confirm.lower() not in ['y', 'n']:
                confirm = raw_input('delete stamp? (y/n) ')
                confirm = confirm.lower()
            if confirm == 'y':
                self.stamps.pop()
            else:
                # if the user says no to the removal of an stamp, we cannot
                # keep deleting stamps after that one, as that could leave the
                # stamps in an inconsistent state.
                print('Aborting removal of stamps')
                break
        self.save_stamps()

    def import_stamps(self, filename):
        """
        Import the stamps from the given file into the main stamps list,
        merging them into the list (removing duplicated entries)
        """
        if not os.path.exists(filename):
            print('[error] ' + filename + 'does not exist')
            return
        if os.path.isdir(filename):
            print('[error] ' + filename + 'is a directory')
            return
        stamps = self.__json_load(filename)
        if not stamps:
            print('[warning] no stamps can be imported from ' + filename)
            return
        self.stamps.extend(stamps)
        self.remove_duplicates()
        self.sort_stamps()
        self.save_stamps()
        print('[warning] ' + str(len(stamps)) + ' stamps merged')
        print('[warning] remember to review the resulting stamps file')
