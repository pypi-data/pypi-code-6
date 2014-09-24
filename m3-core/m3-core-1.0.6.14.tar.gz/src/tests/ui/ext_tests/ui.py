#coding:utf-8
'''
Created on 21.11.2010

@author: akvarats
'''

from m3.ui.ext import windows
from m3.ui.ext import controls
from m3.ui.ext import panels
from m3.ui.ext import fields

class SimpleWindow(windows.ExtWindow):
    '''
    Простое окно, которое не содержит никаких дочерних элементов
    '''
    def __init__(self):
        super(SimpleWindow, self).__init__()
        
        self.ok_button = controls.ExtButton(text=u'ОК')
        self.cancel_button = controls.ExtButton(text=u'Отмена')
        
        self.buttons.extend([self.ok_button, self.cancel_button])
        
class SimpleEditWindow(windows.ExtEditWindow):
    '''
    '''
    def __init__(self):
        super(SimpleEditWindow, self).__init__()
        
        self.form = panels.ExtForm()
        self.named_field = fields.ExtStringField(name='named_string_field')
        self.form.items.extend([self.named_field,
                                fields.ExtStringField(name='unnamed_string_field_0'),
                                fields.ExtStringField(name='unnamed_string_field_1'),
                                fields.ExtDateField(name='unnamed_date_field_1'),])
        
        self.ok_button = controls.ExtButton(text=u'ОК')
        self.cancel_button = controls.ExtButton(text=u'Отмена')
        
        self.buttons.extend([self.ok_button, self.cancel_button])