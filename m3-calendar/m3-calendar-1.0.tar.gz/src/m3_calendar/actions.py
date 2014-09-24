#coding:utf-8
'''
Created on 31.03.2011

@author: akvarats
'''
from datetime import datetime
from m3_calendar.api import M3Calendar
from m3_calendar.models import ExceptedDayTypeEnum
from m3_calendar.ui import M3CalendarWindow, ExceptedDayEditWindow
from m3.ui.actions import ActionPack, Action
from m3.ui.actions.context import ActionContextDeclaration
from m3.ui.actions.dicts.simple import BaseDictionaryModelActions
from m3.ui.actions.results import ExtUIScriptResult, OperationResult, PreJsonResult
from m3.helpers import urls

from models import ExceptedDay

class M3CalendarPack(ActionPack):
    '''Пакет действий для календаря с праздничными и перенесенными днями'''
    url = '/m3-calendar'

    def __init__(self):
        super(M3CalendarPack, self).__init__()
        self.actions.extend([ShowCalendar, SaveCalendarDate, GetDatesToUI])

    def get_list_url(self):
        return urls.get_url('show_calendar')


class ShowCalendar(Action):
    url = '/show_calendar'
    shortname = 'show_calendar'

    def run(self, request, context):
        window = M3CalendarWindow()
        return ExtUIScriptResult(window)

class SaveCalendarDate(Action):
    url = '/save_calendar_date'
    shortname = 'save_calendar_date'

    def context_declaration(self):
        return [ActionContextDeclaration(name='date', required=True, type=str),
                ActionContextDeclaration(name='type', required=True, type=int)]

    def run(self, request, context):
        pydate = datetime.strptime(context.date, '%d.%m.%Y')
        M3Calendar.add_date_to_db(pydate, context.type)
        return OperationResult(success=True)

class GetDatesToUI(Action):
    url = '/get_dates_to_ui'
    shortname = 'get_dates_to_ui'

    def context_declaration(self):
        return [ActionContextDeclaration(name='year', required=True, type=int)]

    def run(self, request, context):
        min_date = datetime(context.year,1,1)
        max_date = datetime(context.year+1,1,1)
        calendar = M3Calendar()
        workdays = calendar.get_days_by_period_from_db(min_date,max_date)
        dayoffs = calendar.days_by_period(min_date, max_date,
                                          (ExceptedDayTypeEnum.DAYOFF,))
        holidays = calendar.days_by_period(min_date, max_date,
                                          (ExceptedDayTypeEnum.HOLIDAY,))

        #Возвращаем для яваскрипта
        dates = [workdays, dayoffs, holidays]

        def make_js_dates(date_list):
            return [datetime.strftime(date,'%m/%d/%Y') for date in date_list]

        [workdays, dayoffs, holidays] = map(make_js_dates, dates)

        return PreJsonResult({'workdays': workdays, 'dayoffs': dayoffs,
                              'holidays': holidays})


class ExceptedDay_DictPack(BaseDictionaryModelActions):
    '''
    Пакет действий для справочника праздничных и перенесенных дней
    '''
    url = '/excepted-days'
    shortname = 'm3-calendar-excepted-days'
    model = ExceptedDay
    add_window = edit_window = ExceptedDayEditWindow

    list_sort_order = ['day', 'name']

    list_columns = [('day', u'Дата', 100),
                    ('name', u'Название', 300),
                    ('type', u'Тип', 300),]
    filter_field = ['day, name',]

    width, height = 700, 400
    
    def get_rows(self, request, context, offset, limit, filter, user_sort=''):
        result = super(ExceptedDay_DictPack, self).get_rows(request, context, offset, limit, filter, user_sort)
        if isinstance(result, dict) and result.has_key('rows'):
            for row in result['rows']:
                row.type = ExceptedDayTypeEnum.values[row.type]
        return result
