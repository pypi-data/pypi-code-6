from dateutil import rrule
import datetime


def get_business_days(alpha, omega, weekoff=None, holidays=None):
    """return a list of business days between (inclusive) the
    from and to limits.
    @type alpha: datetime.datetime
    @type omega: datetime.datetime
    @param weekoff: a list of non working days in a normal week
    @type weekend: list of rrule.weekdays. Ex: [rrule.SA, rrule.SU]
    @param holidays: a list of special non working days
    @type holidays: list of rrule args or dates.
        ex: [{'freq':dateutil.rrule.YEARLY, 'bymonthday':1, 'bymonth':11}]
    """
    # create an rrule.rruleset instance
    dates = rrule.rruleset()

    # this set is INCLUSIVE of alpha and omega
    dates.rrule(rrule.rrule(
        rrule.DAILY, dtstart=alpha, until=omega)
    )

    if weekoff:
        # here's where we exclude the weekend dates
        dates.exrule(rrule.rrule(
            rrule.DAILY, byweekday=weekoff, dtstart=alpha)
        )

    if holidays:
        for holiday in holidays:
            if isinstance(holiday, datetime.datetime):
                dates.exdate(holiday)
            else:
                complete_holiday = {}
                for key in holiday:
                    complete_holiday[key] = holiday[key]
                complete_holiday['dtstart'] = alpha
                dates.exrule(rrule.rrule(**complete_holiday))

    return list(dates)
