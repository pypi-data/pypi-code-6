from setmagic.models import Setting


class SettingsBackend(object):

    '''
    A structure to organize the settings scheme and provide a simple API for
    easier access to all registered settings.
    '''

    settings = property(lambda self: self._settings)

    def __init__(self, settings_defs):
        '''
        Sync settings schema to both the backend and database
        '''

        self.defs = settings_defs

        for setting_def in settings_defs.values():
            try:
                setting = Setting.objects.get(name=setting_def['name'])
            except Setting.DoesNotExist:
                name = setting_def['name']
                setting = Setting(
                    name=name,
                    current_value=self.defs[name].get('default'))

            setting.__dict__.update(**setting_def)
            setting.save()

    def get(self, name):
        return Setting.objects.get(name=name).current_value

    def set(self, name, value):
        Setting.objects.filter(name=name).update(current_value=value)
