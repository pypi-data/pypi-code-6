#coding: utf-8

from m3.ui.ext.all_components import *

__author__ = 'prefer'


class PermissionEditWindow(ExtEditWindow):
    """
    Окно редактирования права в роли пользователя
    """

    def __init__(self, permissions=None, *args, **kwargs):
        super(PermissionEditWindow, self).__init__(*args, **kwargs)

        self.template_globals =  'm3-users/edit-permission.js'

        self.title = u'Редактирование прав'
        self.width = 500


        self.form = self.get_form()

        self.items.append(self.form)

        #  Заполнение sub_permissions
        if permissions is not None:
            assert isinstance(permissions, dict)
            for code, verbose_name in permissions.items():
                setattr(self, '%s' % code, ExtCheckBox(label=verbose_name, name=code))
                self.form.items.append(getattr(self, '%s' % code))

        # js функция из-за динамического формирования cheekbox'ов
        select = '''
            function select(btn, e, baseParams) {
                    var enabled = Ext.getCmp("%s");
                    var on_desktop = Ext.getCmp("%s");''' % (self.chk_enabled.client_id, self.chk_on_desktop.client_id)

        if permissions is not None:
            assert isinstance(permissions, dict)
            for code, verbose_name in permissions.items():
                select += 'var %s = Ext.getCmp("%s");' % ( code, getattr(self, '%s' % code).client_id)
        select += '''
                    var data = {
                        enabled: enabled.getValue(),
                        on_desktop: on_desktop.getValue(),'''
        if permissions is not None:
            assert isinstance(permissions, dict)
            for code, verbose_name in permissions.items():
                select += '%s : %s.getValue(),' % (code, code)
        select +='''
                    }
                    win.fireEvent('closed_ok', data);
                    win.close(true);
                }
            '''

        self.buttons.extend([
            ExtButton(text=u'Сохранить', handler=select),
            ExtButton(text=u'Отмена', handler='cancelForm')
        ])


    def get_form(self, container_class=ExtForm):
        cont = container_class()
        cont.label_width = 200
        cont.padding = '5'
        cont.layout = 'form'
        
        str_name = ExtStringField()
        str_name.read_only = True
        str_name.label = u'Название действия'
        str_name.anchor = '100%'
        
        chk_enabled = ExtCheckBox()
        chk_enabled.label = u'Право выполнения'
        chk_enabled.name = 'enabled'
        
        chk_on_desktop = ExtCheckBox()
        chk_on_desktop.label = u'Отображать в меню пуск и на десктопе'
        chk_on_desktop.name = 'on_desktop'
        
        cont.items.extend([str_name, chk_enabled, chk_on_desktop])
        
        self.str_name = str_name
        self.chk_enabled = chk_enabled
        self.chk_on_desktop = chk_on_desktop
        
        return cont

        