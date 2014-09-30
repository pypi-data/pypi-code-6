from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class QandaAppConfig(AppConfig):

    name = 'qanda'
    verbose_name = _('Frequently Asked Questions')

    def ready(self):
        pass
