import os
from cratis.features import Feature


class AdminThemeSuit(Feature):

    def __init__(self, title='My site'):
        self.title = title

    def configure_settings(self):

        self.append_apps(['suit'])

        self.append_template_processor('django.core.context_processors.request')

        self.settings.SUIT_CONFIG = {
            'ADMIN_NAME': self.title
        }

        self.settings.TEMPLATE_DIRS += (os.path.dirname(os.path.dirname(__file__)) + '/templates/suit-feature',)
