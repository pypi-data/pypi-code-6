import dbsettings


class TestSet(dbsettings.Group):
    maximum_width = dbsettings.PositiveIntegerValue()
    pas = dbsettings.PasswordValue(help_text='aaa', description='qw')


options = TestSet('QWERTY')
