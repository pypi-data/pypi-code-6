#coding:utf-8

from m3.ui.actions.packs import BaseDictionaryModelActions
import ui
import models

class DulType_DictPack(BaseDictionaryModelActions):
    '''
    Справочник "Документы, удостоверяющие личность"
    '''
    url = '/dultype'
    shortname = 'dultype-dictpack'
    
    title = u'Документы, удостоверяющие личность'
    list_columns = [('code', u'Код', 50),('name', u'Наименование')]
    model = models.DulType
    edit_window = ui.DulTypeEditWindow
    
    def __init__(self, *args, **kwargs):
        super(DulType_DictPack,self).__init__(*args,**kwargs)    
        