#coding:utf-8
'''
Created on 25.10.2010

@author: kir
'''
import datetime

from m3.ui.ext.controls.buttons import ExtButton
from m3.ui.ext.shortcuts import js_close_window
from m3.ui.ext.fields.simple import ExtComboBox, ExtDateField, ExtTextArea
from m3.ui.ext.panels.grids import ExtObjectGrid
from m3.ui.ext.misc.store import ExtJsonStore
from m3.ui.ext.containers.container_complex import ExtContainerTable
from m3.ui.ext.containers.forms import ExtPanel
from m3.ui.ext.windows.window import ExtWindow
        
class ExtLogsWindow(ExtWindow):
    def __init__(self, window_params=None, *args, **kwargs):
        super(ExtLogsWindow, self).__init__(*args, **kwargs)
        self.__dict__.update(window_params)
        self.title=u'Просмотр логов'
        self.min_width, self.min_height = self.width, self.height = 800, 500
        self.modal = False
        self.maximizable = True
        self.closable = True
        self.layout = 'border'
        self.layout_config = {'align': 'stretch'}
        self.template_globals = 'ui-js/logview.js'
        
        self.grid = ExtObjectGrid(flex=1, region = 'center')
        self.grid.add_column(header=u'Дата и время', data_index='date', width=22)
        self.grid.add_column(header=u'Текст сообщения', data_index='message')
        self.grid.add_column(header=u'Польное тело сообщения', data_index='full', 
                             hidden=True)
        grid_store = ExtJsonStore(auto_load=False, total_property='total', root='rows')
        self.store = grid_store
        self.grid.set_store(grid_store) 
        
        self.start_date = ExtDateField(
            label=u'С', 
            name='start_date',
            allow_blank=False, 
            hide_today_btn=True,
            value = datetime.datetime.now()
        )
        
        self.end_date = ExtDateField(
            label=u'по', 
            name='end_date',
            allow_blank=False, 
            hide_today_btn=True,
            value = datetime.datetime.now()
        )          
        self.log_files_combo  = ExtComboBox(
            label = u'Выберите файл',
            editable = False, 
            display_field = 'name',
            value_field = 'name',
            mode = 'remote',
            trigger_action_all = 'true'
        )
        
        # ContainerTable on top include date and log_files_combo
        top_container_table = ExtContainerTable(columns=6, rows=1, height=22, 
                                                region='north')
        top_container_table.set_item(row=0, col=1, cmp=self.start_date, 
                                     width=120, label_width = 15)
        top_container_table.set_item(row=0, col=3, cmp=self.end_date,
                                     width=120, label_width = 15)
        top_container_table.set_item(row=0, col=5, cmp=self.log_files_combo,
                                     width=300)
        top_container_table.set_properties(col_num=2, width=30)
        top_container_table.set_properties(col_num=4, width=30)
        top_container_table.set_properties(col_num=0, width=30)
        
        self.file_context_panel = ExtPanel(
                                      title = u'Содержимое',
                                      height=200, 
                                      padding = 5, 
                                      body_cls='x-window-mc',
                                      region = 'south',
                                      layout='fit',
                                      collapsible = True,
                                      split = True)
        self.text_field = ExtTextArea(read_only=True)
        self.file_context_panel.items.append(self.text_field)
        
        
        self.items.extend([top_container_table, self.grid, self.file_context_panel])
        
        #Button's
        self.update_button = ExtButton(text=u'Обновить', hidden=True)
        self.update_button.handler = 'callBackfunc_combo'
        close_button = ExtButton(text=u'Закрыть')
        close_button.handler = js_close_window(self, True)
        self.buttons.extend([self.update_button, close_button])