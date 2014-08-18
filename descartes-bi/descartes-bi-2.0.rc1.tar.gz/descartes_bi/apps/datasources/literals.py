from django.utils.translation import ugettext_lazy as _

DATASOURCE_FORMAT_TEXT = 1
DATASOURCE_FORMAT_JSON = 2

DATASOURCE_FORMAT_CHOICES = (
    (DATASOURCE_FORMAT_TEXT, _('Text')),
    (DATASOURCE_FORMAT_JSON, _('JSON')),
)
