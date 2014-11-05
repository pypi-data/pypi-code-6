from django.db.models import DateTimeField
from datetime import timedelta
from django.core.exceptions import FieldError

class ExpireField(DateTimeField):
    def __init__(self, verbose_name=None, name=None, **kwargs):
        self.duration = kwargs.pop('duration')
        if not isinstance(self.duration, timedelta):
            raise FieldError
        super(ExpireField, self).__init__(verbose_name, name, **kwargs)
