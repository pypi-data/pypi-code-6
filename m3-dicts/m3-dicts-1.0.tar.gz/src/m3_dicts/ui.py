#coding:utf-8

from m3.ui.ext import windows
from m3.ui.ext import fields 
from m3.ui.ext.containers import forms
from m3.ui.ext.controls import buttons


class DulTypeEditWindow(windows.ExtEditWindow):
    '''
    Окно редактирования документа, удостоверяющего личность
    '''
    def __init__(self, create_new = True, *args, **kwargs):
        super(DulTypeEditWindow, self).__init__(*args, **kwargs)
        self.width, self.height = 430, 123
        self.min_width, self.min_height = self.width, self.height
        self.title = u'Новый документ' if create_new else u'Редактирование документа'

        self._code = fields.ExtStringField(anchor='100%', name = 'code', 
                                           max_length = 20, label = u'Код')
        self._name = fields.ExtStringField(anchor='100%', name = 'name', 
                                           max_length = 200, label = u'Наименование')
        
        self.form = forms.ExtForm()
        self.form.items.extend([
            self._code,
            self._name
        ])
        
        # Кнопки
        self.buttons.extend([
            buttons.ExtButton(text=u'Сохранить', handler='submitForm'),
            buttons.ExtButton(text=u'Закрыть', handler='cancelForm')
        ])           