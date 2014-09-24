#coding: utf-8

from m3.ui.ext.windows import ExtWindow
from m3.ui.ext.containers.forms import ExtPanel
from m3.ui.ext.fields.simple import ExtStringField


class TestOne(ExtWindow):
    '''©
    Простой класс'''

    def __init__(self, *args, **kwargs):
        super(TestOne, self).__init__(*args, **kwargs)
        self.initialize()

    def initialize(self):
        '''©
        AUTOGENERATIONS! 
        Do not Touch!
        Не редактировать!!        
        '''
        self.width = 200
        self.height = 300
        self.title = u'Простое окно'
        self.layout = 'fit'
        panel1 = ExtPanel()
        panel1.title = u'Простое название'
        panel1.layout = 'form'
        field1 = ExtStringField()
        field1.label = u'Простое поле'
        panel1.items.extend([field1])
        self.items.extend([panel1])

    def ata(self):
        pass