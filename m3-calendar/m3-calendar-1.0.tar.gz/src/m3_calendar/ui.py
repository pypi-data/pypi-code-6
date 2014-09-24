#coding:utf-8
'''
Created on 31.03.2011

@author: akvarats
'''
import datetime
from m3.helpers import urls
from m3.helpers.icons import Icons
from m3.ui.ext.containers.containers import ExtContainer, ExtToolBar
from m3.ui.ext.containers.forms import ExtPanel
from m3.ui.ext.controls.buttons import ExtButton
from m3.ui.ext.windows.window import ExtWindow
from m3.ui.gears.edit_windows import GearEditWindow
from m3.ui.ext.fields.simple import ExtDateField, ExtComboBox, ExtStringField, ExtNumberField
from m3_calendar.models import ExceptedDayTypeEnum
from m3.ui.ext.misc.store import ExtDataStore


class M3CalendarWindow(ExtWindow):
    """
    Окно с маленькими календарями для всех месяцев в году
    """
    def __init__(self, *args, **kwargs):
        super(M3CalendarWindow, self).__init__(*args, **kwargs)
        self.layout = 'auto'
        self.template_globals = 'showM3Calendar.js'
        self.date_save_url = urls.get_url('save_calendar_date')
        self.get_date_url = urls.get_url('get_dates_to_ui')
        self.resizable = False
        self.title = u'Календарь рабочих и выходных дней'

        #Высоту и ширину подгонял почти попиксельно.
        self.width = 734
        self.height = 550

        self._initialize()
        self._init_calendar_containers()

    def _initialize(self):
        tlb_calendar = ExtToolBar()
        tlb_calendar.layout = 'toolbar'

        text_year = ExtToolBar.TextItem()
        text_year.text = u'Выберите год:'

        toolbar_spacer = ExtToolBar.Spacer()
        toolbar_spacer.width = 5

        btn_previous_year = ExtButton()
        btn_previous_year.icon_cls = Icons.ARROW_LEFT
        btn_previous_year.handler = 'previousYear'

        year_field = ExtNumberField()
        year_field.width = 35
        year_field.read_only = True
        year_field.value = datetime.datetime.now().year

        btn_next_year = ExtButton()
        btn_next_year.icon_cls = Icons.ARROW_RIGHT
        btn_next_year.handler = 'nextYear'

        self.top_bar = tlb_calendar

        tlb_calendar.items.extend([text_year, toolbar_spacer, btn_previous_year, year_field, btn_next_year])

        self.tlb_calendar = tlb_calendar
        self.text_year = text_year
        self.toolbar_spacer = toolbar_spacer
        self.btn_previous_year = btn_previous_year
        self.year_field = year_field
        self.btn_next_year = btn_next_year

    def _init_calendar_containers(self):
        table_container = ExtContainer(layout='table', height=600, width=800)
        table_container.layout_config = dict(columns=4, rows=3)
        self.table_container = table_container

        for i in xrange(12):
            self.table_container.items.append(ExtPanel(layout='fit'))

        self.items.append(self.table_container)

        self._listeners['show'] = 'generateCalendars'


class ExceptedDayEditWindow(GearEditWindow):
    '''
    Окно редактирования праздничного дня
    '''
    def __init__(self, create_new=False, *args, **kwargs):
        super(ExceptedDayEditWindow, self).__init__(create_new, *args, **kwargs)
        self.title = u'%s праздничного / выходного дня' % (u'Создание' if create_new else u'Редактирование')
        self.frozen_size(300, 200)
        self.form.layout = 'form'
        self.layout = 'fit'
        
        self.name_field = ExtStringField(max_length = 200, 
                                         label = u'Название', 
                                         name = 'name', 
                                         anchor='100%', 
                                         allow_blank=False) # наименование выключенного дня
        self.day_field  = ExtDateField(label=u'День',
                                       name='day',
                                       hide_today_btn=True,
                                       allow_blank=False,
                                       anchor="100%")
        self.type_field = ExtComboBox(label=u'Тип',
                                      name='type',
                                      trigger_action_all=True,
                                      value_field='id',
                                      display_field='name',
                                      allow_blank=False,
                                      value=ExceptedDayTypeEnum.HOLIDAY,
                                      editable=False,
                                      anchor="100%")
        self.type_field.set_store(ExtDataStore(ExceptedDayTypeEnum.get_items()))
        self.form.items.extend([self.name_field,
                                self.day_field,
                                self.type_field,])