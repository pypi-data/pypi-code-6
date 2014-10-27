#-*- coding: utf-8 -*-

from bootstrap3_wysihtml5x.fields import Wysihtml5TextField
from bootstrap3_wysihtml5x.widgets import Wysihtml5TextareaWidget

class AdminWysihtml5TextFieldMixin(object):
    """Mixin for ModelAdmin subclasses to provide custom widget for ``Wysihtml5TextField`` fields."""
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, Wysihtml5TextField):
            return db_field.formfield(widget=Wysihtml5TextareaWidget)
        sup = super(AdminWysihtml5TextFieldMixin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)
