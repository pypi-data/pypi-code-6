from django.template import Library
from django.utils.timezone import get_current_timezone
from datetime import datetime, timedelta
register = Library()

@register.filter
def fromtimestamp(value):
    date = datetime(
        1970, 1, 1, 0, 0, 0
    ) + timedelta(
        seconds = int(value)
    )

    return date.replace(
        tzinfo = get_current_timezone()
    )
