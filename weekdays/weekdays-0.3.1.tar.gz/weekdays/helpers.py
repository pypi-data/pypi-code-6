import datetime
from weekdays import get_business_days
import calendar


class BusinessCalendar(calendar.Calendar):

    def __init__(self, weekstartday, weekoff, holidays):

        self.weekstartday = weekstartday
        self.weekoff = weekoff
        self.holidays = holidays

        super(BusinessCalendar, self).__init__(weekstartday)

    def get_month_business_days(self, year, month):
        """given a year and a month returns the business days for this month
        respecting the rules that were give during calendar initialisation.
        """
        start = datetime.datetime(year, month, 1, 0, 0)
        # get last day of the desired month
        lastdaynum = calendar.monthrange(year, month)[1]
        end = datetime.datetime(year, month, lastdaynum, 0, 0)

        return get_business_days(start, end, self.weekoff, self.holidays)

    def get_weeks_business_days(self, year, month):
        """given an year and month returns the business days for this month
        ordered in lists of weeks.
        """
        business_weeks = []
        # this is the naive list of days sorted in weeks
        allweeksdays = self.monthdatescalendar(year, month)

        monthbusinessdays = self.get_month_business_days(year, month)

        for week in allweeksdays:
            weekbusinessdays = []
            for day in week:
                daydt = datetime.datetime(day.year, day.month, day.day, 0, 0)
                if daydt in monthbusinessdays:
                    weekbusinessdays.append(daydt)

            business_weeks.append(weekbusinessdays)

        return business_weeks

    def get_weeks_daycount(self, year, month):
        """given a year and month returns a list of business days count
        for all the weeks of the month.
        ie: [0, 5, 4, 5, 5]
        """
        return [
            len(week) for week in self.get_weeks_business_days(year, month)
        ]
