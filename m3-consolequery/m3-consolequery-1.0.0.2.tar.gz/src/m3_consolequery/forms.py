#coding:utf-8
'''
Created on 14.12.2010

@author: Камилла
'''

from m3.ui.ext.controls.buttons import ExtButton
from m3.ui.ext.shortcuts import js_close_window
from m3.ui.ext.containers.grids  import ExtGrid
from m3.ui.ext.fields.simple import  ExtTextArea,  ExtStringField
from m3.ui.ext.fields.complex import ExtDictSelectField
import helpers as admin_helpers

from m3.ui.ext.containers.container_complex import ExtContainerTable
from m3.ui.ext.misc.store import ExtJsonStore

from m3.ui.ext.containers.forms import ExtForm
from m3.ui.ext.windows.window import ExtWindow

class ExtQueryConsoleWindow(ExtWindow):
    '''
    Окно для вывода запроса
    '''
    def __init__(self, window_params, *args, **kwargs):
        super(ExtQueryConsoleWindow, self).__init__(*args, **kwargs)
        self.template_globals = 'ui-js/ExtQueryConsoleWindow.js'
        self.title = u'Консоль запросов'
        self.height = self.min_height = 600
        self.width = self.min_width = 900
        self.modal = False
        self.minimizable = True
        self.maximizable = True
        self.layout = 'vbox'
        
        self.layout_config['align'] = 'stretch'
        
        self.__dict__.update(window_params)
        
        query_panel = ExtContainerTable(columns=3, rows=2, height = 110)
        
        #Поле для ввода запроса
        self.query_str = ExtTextArea(label = u'Текст запроса', name = 'query_str',
                                        anchor = '100%')
        #Поле выбора запроса из списка
        self.query_selected = ExtDictSelectField(
            label = u'Запрос',
            name='query_selected',  
            ask_before_deleting=False,
            display_field='name',
            value_field='id',
            hide_trigger=False,
            hide_edit_trigger=True,
            width = 500
        )
        self.query_selected.pack = 'CustomQueries_DictPack'
        
        #Buttons
        load_button = ExtButton(text = u'Загрузить', handler = 'load_selected_query')
        save_button = ExtButton(text = u'Сохранить', handler = 'save_new_query')
        
        
        query_panel.set_item(0, 0, self.query_selected, colspan=0)
        query_panel.set_item(0, 1, load_button, colspan=0)
        query_panel.set_item(0, 2, save_button, colspan=0)
        query_panel.set_item(1, 0, self.query_str, colspan=3)
        query_panel.set_row_height(1, 70)
        
        
        self.buttons.append(ExtButton(text = u'Сделать запрос', handler = 'make_query'))
        self.buttons.append(ExtButton(text = u'Закрыть', handler = js_close_window(self, True)))
        #Отображение результата запроса
        self.grid = ExtGrid(layout='fit', flex=1)
        grid_store = ExtJsonStore(auto_load=False, total_property='total', root='rows')
        self.store = grid_store
        self.grid.set_store(grid_store) 
        
        self.items.extend([query_panel, self.grid])
        
        self.init_component(*args, **kwargs)
        
class ExtNewQueryWindow(ExtWindow):
    '''
    Окно для сохранения нового запроса
    '''
    def __init__(self, window_params, *args, **kwargs):
        super(ExtNewQueryWindow, self).__init__(*args, **kwargs)
        self.template_globals = 'ui-js/ExtNewQueryWindow.js'
        self.title = u'Сохранение нового запроса'
        self.height = self.min_height = 150
        self.width = self.min_width = 300
        self.modal = False       
        
        self.__dict__.update(window_params)
        
        #Поле для ввода наименования запроса
        try:
            query_id = window_params.get('query_name','')
            query_name = admin_helpers.load_query(query_id, True)
        except:
            query_name = None 
        self.query_name = ExtStringField(label=u'Наименование', name = 'query_name',
                                        anchor = '100%', value = query_name)
        #button
        self.save_button = ExtButton(text = u'Сохранить', handler = 'save_query')
        self.close_button = ExtButton(text = u'Закрыть', handler = js_close_window(self, True))
        form = ExtForm(label_align = 'top')
        form.items.extend([self.query_name])
        
        self.items.extend([form])
        
        self.buttons.extend([self.save_button, self.close_button])
        
        self.init_component(*args, **kwargs)     
