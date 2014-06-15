from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import widgets as admin_widgets
from south.modelsinspector import add_introspection_rules


STATUS_CODES = (
    (0, _('Inactive')),
    (1, _('Active')),
)

class StatusField(models.IntegerField):
    def __init__(
        self, choices=STATUS_CODES, max_length=3, default=1, verbose_name=_('Status'), help_text=None
    ):
        super(StatusField, self).__init__(
            choices=choices,
            max_length=max_length,
            default=default,
            verbose_name=verbose_name,
            help_text=help_text
        )

    def get_db_prep_value(self, value, connection=None, prepared=None):
        if value is None or value == '':
            return 1
        return int(value)


class HTMLField(models.TextField):
    # Lasciamo questa classe solo per evitare di passarci tutti i modelli
    # e cambiare l'import dell html field
    pass
try:
    from tinymce import models as tinymce_models
    class HTMLFieldTinyMCE(tinymce_models.HTMLField):
        # Lasciamo questa classe solo per evitare di passarci tutti i modelli
        # e cambiare l'import dell html field
        pass
except:
    class HTMLFieldTinyMCE(HTMLField):
        # Lasciamo questa classe solo per evitare di passarci tutti i modelli
        # e cambiare l'import dell html field
        pass
# Add introspection rules for migrate
rules = [
    (
        (StatusField, ),
        [],
        {
            "max_length": ["max_length", {"default": 3}],
            "default": ["default", {"default": 1}],
        },
    ),
    (
        (HTMLField, ),
        [],
        {},
    ),
]

add_introspection_rules(rules, ["^jmb\.core\.db\.fields",])
